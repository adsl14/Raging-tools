using System.IO;
using System;
using System.Collections.Generic;
using System.Linq;


class Swizzle
{

    public static Int32 calcZOrder(int xPos, int yPos) //Credit to user aggsol from https://stackoverflow.com/questions/12157685/z-order-curve-coordinates, whose solution is based on http://graphics.stanford.edu/~seander/bithacks.html
    {
        Int32[] MASKS = { 0x55555555, 0x33333333, 0x0F0F0F0F, 0x00FF00FF};
        Int32[] SHIFTS = { 1, 2, 4, 8 };

        Int32 x = xPos;
        Int32 y = yPos;

        x = (x | (x << SHIFTS[3])) & MASKS[3];
        x = (x | (x << SHIFTS[2])) & MASKS[2];
        x = (x | (x << SHIFTS[1])) & MASKS[1];
        x = (x | (x << SHIFTS[0])) & MASKS[0];

        y = (y | (y << SHIFTS[3])) & MASKS[3];
        y = (y | (y << SHIFTS[2])) & MASKS[2];
        y = (y | (y << SHIFTS[1])) & MASKS[1];
        y = (y | (y << SHIFTS[0])) & MASKS[0];

        int result = x | (y << 1);
        return result;
    }

    public static byte[] unswizzle(byte[] filedata, Int32 size, Int32 width, Int32 height, List<int> indexes)
    {
        int index = -1;
        List<byte> swizzled = new List<byte>();

        // 1. y = 0, y < width; x = 0, x < width -> 0,0 to width, width
        // 2. y = 0, y < width; x = width, x < height -> width,0 to height, width
        // 3. y = width, y < height; x = 0, x < width -> 0,width to width, height
        // 4. y = width, y < height; x = width, x < height width,width to height, height
        
        // 1.
        for (int y = 0; y < width; y++)
        {
            for (int x = 0; x < width; x++)
            {
                index = calcZOrder(x, y);

                if (size > index * 4) //check that the index is available (might not be when we have a square bigger than the original width or height)
                { 
                    swizzled.Add(filedata[index * 4]);
                    indexes.Add(index * 4);
                    if (size > index * 4 + 1)
                    {
                        swizzled.Add(filedata[index * 4 + 1]);
                        indexes.Add(index * 4 + 1);
                        if (size > index * 4 + 2)
                        {
                            swizzled.Add(filedata[index * 4 + 2]);
                            indexes.Add(index * 4 + 2);
                            if (size > index * 4 + 3)
                            {
                                swizzled.Add(filedata[index * 4 + 3]);
                                indexes.Add(index * 4 + 3);
                            }
                        }
                    }
                }
            }
        }

        // 2.
        for (int y = 0; y < width; y++)
        {
            for (int x = width; x < height; x++)
            {
                index = calcZOrder(x, y);

                if (size > index * 4) //check that the index is available (might not be when we have a square bigger than the original width or height)
                { 
                    swizzled.Add(filedata[index * 4]);
                    indexes.Add(index * 4);
                    if (size > index * 4 + 1)
                    {
                        swizzled.Add(filedata[index * 4 + 1]);
                        indexes.Add(index * 4 + 1);
                        if (size > index * 4 + 2)
                        {
                            swizzled.Add(filedata[index * 4 + 2]);
                            indexes.Add(index * 4 + 2);
                            if (size > index * 4 + 3)
                            {
                                swizzled.Add(filedata[index * 4 + 3]);
                                indexes.Add(index * 4 + 3);
                            }
                        }
                    }
                }
            }
        }

        // 3.
        for (int y = width; y < height; y++)
        {
            for (int x = 0; x < width; x++)
            {
                index = calcZOrder(x, y);

                if (size > index * 4) //check that the index is available (might not be when we have a square bigger than the original width or height)
                { 
                    swizzled.Add(filedata[index * 4]);
                    indexes.Add(index * 4);
                    if (size > index * 4 + 1)
                    {
                        swizzled.Add(filedata[index * 4 + 1]);
                        indexes.Add(index * 4 + 1);
                        if (size > index * 4 + 2)
                        {
                            swizzled.Add(filedata[index * 4 + 2]);
                            indexes.Add(index * 4 + 2);
                            if (size > index * 4 + 3)
                            {
                                swizzled.Add(filedata[index * 4 + 3]);
                                indexes.Add(index * 4 + 3);
                            }
                        }
                    }
                }
            }
        }

        // 4.
        for (int y = width; y < height; y++)
        {
            for (int x = width; x < height; x++)
            {
                index = calcZOrder(x, y);

                if (size > index * 4) //check that the index is available (might not be when we have a square bigger than the original width or height)
                { 
                    swizzled.Add(filedata[index * 4]);
                    indexes.Add(index * 4);
                    if (size > index * 4 + 1)
                    {
                        swizzled.Add(filedata[index * 4 + 1]);
                        indexes.Add(index * 4 + 1);
                        if (size > index * 4 + 2)
                        {
                            swizzled.Add(filedata[index * 4 + 2]);
                            indexes.Add(index * 4 + 2);
                            if (size > index * 4 + 3)
                            {
                                swizzled.Add(filedata[index * 4 + 3]);
                                indexes.Add(index * 4 + 3);
                            }
                        }
                    }
                }
            }
        }

        filedata = swizzled.ToArray();

        return filedata.ToArray();
    }

    public static void swizzle(byte[] filedataSwizzled, byte[] filedataUnSwizzled, string[] indexes)
    {
        int indexUnSwizzled = 0;
        foreach(string index in indexes)
        {
            filedataSwizzled[Int32.Parse(index)] = filedataUnSwizzled[indexUnSwizzled];
            indexUnSwizzled++;
        }
    }

    public static byte[] fix_orientation_image(byte[] imageData, Int32 width, Int32 height)
    {
        Int32 widthImageArray = width * 4;
        Int32 indexStart = 0;
        byte[] rowPixelsImage = new byte[widthImageArray];
        List<byte> orientedImage = new List<byte>();

        for(Int32 j = height - 1; j >= 0; j--)
        {
            indexStart = width * 4 * j;
            Buffer.BlockCopy(imageData, indexStart, rowPixelsImage, 0, widthImageArray);
            orientedImage.AddRange(rowPixelsImage);
        }

        return orientedImage.ToArray();
    }

    public static byte[] invertBytes(byte[] imageData, Int32 size)
    {
        List<byte> imageFixedColors = new List<byte>();
        byte[] data4Bytes = new byte[4];

        for(Int32 i = 0; i < size; i+=4)
        {
            Buffer.BlockCopy(imageData, i, data4Bytes, 0, 4);
            Array.Reverse(data4Bytes, 0, 4);
            imageFixedColors.AddRange(data4Bytes);
        }

        return imageFixedColors.ToArray();

    }

    static void Main(string[] args)
    {
        bool unswizzleFlag = true, found = false;

        // Get the option. -u is to unswizzle. -s is to swizzle
        for(int i = 0; i < args.Length; i++){
            if(args[i] == "-s"){
                unswizzleFlag = false;
                found = true;
                break;
            } else if(args[i] == "-u")
            {
                found = true;
                break;
            }
        }

        if(found)
        {
            if(unswizzleFlag)
            {
                List<int> indexes = new List<int>();

                // Read the image in bytes
                byte[] fullData = File.ReadAllBytes(args[0]);

                // Size image
                byte[] tempData = new byte[4];
                Buffer.BlockCopy(fullData, 2, tempData, 0, 4);
                Int32 size = BitConverter.ToInt32(tempData, 0) - 54;

                // Width
                Buffer.BlockCopy(fullData, 18, tempData, 0, 4);
                Int32 width = BitConverter.ToInt32(tempData, 0);

                // Height
                Buffer.BlockCopy(fullData, 22, tempData, 0, 4);
                Int32 height = BitConverter.ToInt32(tempData, 0);

                // The data itself
                byte[] filedata = new byte[size];
                Buffer.BlockCopy(fullData, 54, filedata, 0, size);

                // unswizzle algorithm
                Console.WriteLine("Unswizzling image...");
                byte[] unswizzled = unswizzle(filedata, size, width, height, indexes);

                // oriented image
                Console.WriteLine("Orienting image...");
                byte[] orientedImage = fix_orientation_image(unswizzled, width, height);

                // fix colors
                Console.WriteLine("Fixing colors...");
                byte[] fixedColorsImage = invertBytes(orientedImage, size);

                // Create the output
                var myfile = File.Create("tempUnSwizzledImage");
                myfile.Write(fixedColorsImage,0,size);
                myfile.Close();

                // Create a txt with the indexes
                StreamWriter sw = new StreamWriter("Indexes.txt");
                foreach (Int32 index in indexes)
                    sw.Write(index.ToString() + ";");
                sw.Close();
            } else 
            {
                // Read the image in bytes
                byte[] fullDataSwizzled = File.ReadAllBytes(args[0]);
                byte[] fullDataUnSwizzled = File.ReadAllBytes(args[1]);

                // Get the indexes
                StreamReader sr = new StreamReader(args[2]);
                String line = sr.ReadLine();
                // Get the indexes
                string[] indexes = line.Split(';');
                Array.Resize(ref indexes, indexes.Length - 1);

                // Size image
                byte[] tempData = new byte[4];
                Buffer.BlockCopy(fullDataSwizzled, 2, tempData, 0, 4);
                Int32 size = BitConverter.ToInt32(tempData, 0) - 54;

                // Width
                Buffer.BlockCopy(fullDataSwizzled, 18, tempData, 0, 4);
                Int32 width = BitConverter.ToInt32(tempData, 0);

                // Height
                Buffer.BlockCopy(fullDataSwizzled, 22, tempData, 0, 4);
                Int32 height = BitConverter.ToInt32(tempData, 0);

                // unfix colors
                Console.WriteLine("Unfixing colors...");
                byte[] orientedImage = invertBytes(fullDataUnSwizzled, size);

                // reoriented image
                Console.WriteLine("Reverting image...");
                byte[] unswizzled = fix_orientation_image(orientedImage, width, height);

                Console.WriteLine("Swizzling image...");
                swizzle(fullDataSwizzled, unswizzled, indexes);

                // Create the output
                var myfile = File.Create("tempSwizzledImageModified");
                myfile.Write(fullDataSwizzled,0,size);
                myfile.Close();

            }
        }
        
    }
}