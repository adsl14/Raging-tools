using System.IO;
using System;
using System.Collections.Generic;
using System.Linq;


class Swizzle
{
    public static Int32 xgAddress2dTiled(bool axisX, Int32 offset, Int32 width, Int32 texelPitch)
    {
        Int32 alignedWidth = 0;
        Int32 logBpp = 0;
        Int32 offsetB = 0;
        Int32 offsetT = 0;
        Int32 offsetM = 0;
        Int32 macroX = 0;
        Int32 macroY = 0;
        Int32 tile = 0;
        Int32 macro = 0;
        Int32 micro = 0;
        Int32 result = 0;

        alignedWidth = (width + 31) & ~31;

        logBpp = (texelPitch >> 2) + ((texelPitch >> 1) >> (texelPitch >> 2));
        offsetB = offset << logBpp;
        offsetT = ((offsetB & ~4095) >> 3) + ((offsetB & 1792) >> 2) + (offsetB & 63);
        offsetM = offsetT >> (7 + logBpp);

        if (axisX)
        {
            macroX = ((offsetM % (alignedWidth >> 5)) << 2);
            tile = ((((offsetT >> (5 + logBpp)) & 2) + (offsetB >> 6)) & 3);
            macro = (macroX + tile) << 3;
            micro = ((((offsetT >> 1) & ~15) + (offsetT & 15)) &
                     ((texelPitch << 3) - 1)) >> logBpp;

            result = macro + micro;
        }
        else
        {
            macroY = (((int)(offsetM / (alignedWidth >> 5))) << 2);
            tile = ((offsetT >> (6 + logBpp)) & 1) + (((offsetB & 2048) >> 10));
            macro = (macroY + tile) << 3;
            micro = ((((offsetT & (((texelPitch << 6) - 1) & ~31)) + ((offsetT & 15) << 1)) >> (3 + logBpp)) & ~1);

            result = macro + micro + ((offsetT & 16) >> 4);
        }

        return result;
    }

    public static byte[] convertLinearTexture(byte[] data, String direction, Int32 height, Int32 width, String textureType)
    {
        Int32 blockSize = 0;
        Int32 texelPitch = 0;
        Int32 blockWidth = 0;
        Int32 blockHeight = 0;
        Int32 blockOffset = 0;
        Int32 srcOffset = 0;
        Int32 destOffset = 0;
        Int32 x = 0;
        Int32 y = 0;

        // DXT1
        if (String.Equals(textureType, "DXT1"))
        {
            blockSize = 4;
            texelPitch = 8;
        }
        // DXT3, DXT5 or ATI2
        else if (String.Equals(textureType, "DXT3") || String.Equals(textureType, "DXT5") || String.Equals(textureType, "ATI2"))
        {
            blockSize = 4;
            texelPitch = 8;
        }
        else
            throw new InvalidOperationException("Unknown DXT type");

        blockWidth = (int)(width / blockSize);
        blockHeight = (int)(height / blockSize);

        byte[] newData = new byte[data.Length];
        for (int j = 0; j < blockHeight; ++j)
        {
            for (int i = 0; i < blockWidth; ++i)
            {
                blockOffset = j * blockWidth + i;

                x = xgAddress2dTiled(true, blockOffset, blockWidth, texelPitch);
                y = xgAddress2dTiled(false, blockOffset, blockWidth, texelPitch);

                srcOffset = j * blockWidth * texelPitch + i * texelPitch;
                destOffset = y * blockWidth * texelPitch + x * texelPitch;

                if (destOffset < data.Length)
                {
                    // Direction -> to
                    if (String.Equals(direction,"to"))
                    {
                        int k = srcOffset;
                        for(int l = destOffset; l < (destOffset+texelPitch); l++)
                        {
                            newData[l] = data[k];
                            ++k;
                        }
                    }
                    // Direction -> from
                    else
                    {
                        int k = destOffset;
                        for(int l = srcOffset; l < (srcOffset+texelPitch); l++)
                        {
                            newData[l] = data[k];
                            ++k;
                        }
                    }
                }
            }
        }

        return newData;
    }

    public static byte[] handleData(byte[] data, Int32 width, Int32 height, String textureType, bool action)
    {
        String direction;
        byte aux;
        if (action) 
            direction = "to";
        else 
            direction = "from";

        data = convertLinearTexture(data, direction, height, width, textureType);

        for (int i = 0; i < data.Length; i=i+4)
        {
            // Swap bytes
            aux = data[i];
            data[i] = data[i + 1];
            data[i + 1] = aux;

            aux = data[i + 2];
            data[i + 2] = data[i + 3];
            data[i + 3] = aux;
        }

        return data;
    }

    public static Int32 process(List<byte> newData, byte[] data, Int32 width, Int32 height, Int32 mipmapCount, String textureType, bool action)
    {
        List<byte> tempData = new List<byte>();
        Int32 newDataSize = 0;
        Int32 currentWidth = width;
        Int32 currentHeight = height;
        Int32 currentMipMapCount = mipmapCount;
        Int32 limit = 0;

        while(currentMipMapCount > 0)
        {
            newDataSize = tempData.Capacity;
            if (action == true && currentWidth <= 64 && currentHeight <= 64)
                break;
            // DXT1
            else if (String.Equals(textureType, "DXT1"))
                limit = newDataSize + (int)(currentWidth * currentHeight / 2);
            else
                limit = newDataSize + (int)(currentWidth * currentHeight);

            // Get subarray from the original texture data
            byte[] subData = new byte[limit-newDataSize];
            Buffer.BlockCopy(data, newDataSize, subData, 0, limit-newDataSize);

            // Append the result to the temp texture data.
            tempData.AddRange(handleData(subData, currentWidth, currentHeight, textureType, action));
            tempData = tempData.ToList();

            currentWidth = (int)(currentWidth / 2);
            currentHeight = (int)(currentHeight / 2);
            --currentMipMapCount;
        }

        mipmapCount -= currentMipMapCount;
        
        // Return the result to the 'newData' in order to save it in disk
        newData.AddRange(tempData);

        return mipmapCount;
    }

    static void Main(string[] args)
    {
        bool unswizzleFlag = true, found = false;
        String outputName = "";
        List<byte> newData = new List<byte>();
        byte[] tempData = new byte[4];

        // Get the option. -u is to unswizzle. -s is to swizzle
        for(int i = 0; i < args.Length; i++){
            if(args[i] == "-s"){
                unswizzleFlag = false;
                outputName = "tempSwizzledXbox360Image";
                found = true;
                break;
            } else if(args[i] == "-u")
            {
                found = true;
                outputName = "tempUnSwizzledXbox360Image";
                break;
            }
        }

        if(found)
        {
            // Read the image in bytes
            byte[] fullData = File.ReadAllBytes(args[0]);

            // Height
            Buffer.BlockCopy(fullData, 12, tempData, 0, 4);
            Int32 height = BitConverter.ToInt32(tempData, 0);

            // Width
            Buffer.BlockCopy(fullData, 16, tempData, 0, 4);
            Int32 width = BitConverter.ToInt32(tempData, 0);

            // mipMaps
            Buffer.BlockCopy(fullData, 28, tempData, 0, 4);
            Int32 mipMaps = BitConverter.ToInt32(tempData, 0);

            // Encoding
            Buffer.BlockCopy(fullData, 84, tempData, 0, 4);
            String encoding = System.Text.Encoding.UTF8.GetString(tempData);

            // Get original texture data
            Int32 textureDataSize = fullData.Length-128;
            byte[] textureData = new byte[textureDataSize];
            Buffer.BlockCopy(fullData, 128, textureData, 0, textureDataSize);

            // Swizzle/Unswizzle algorithm
            mipMaps = process(newData, textureData, width, height, mipMaps, encoding, unswizzleFlag);

            // Create the output texture
            var myfile = File.Create(outputName);
            myfile.Write(newData.ToArray() ,0, newData.Capacity);
            myfile.Close();

            // Write the mipmaps
            var myfile2 = File.Create("mipMaps");
            myfile2.Write(BitConverter.GetBytes(mipMaps) ,0, 4);
            myfile2.Close();
        }      
    }
}