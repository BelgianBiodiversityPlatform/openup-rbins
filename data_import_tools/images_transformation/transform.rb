require 'RMagick'
include Magick

require 'fileutils'
require 'find'
require 'pp' # debugging purposes only
require './rmagick_text_util'
include RMagickTextUtil

require 'csv'

SOURCE_IMAGE_DIR = "/home/nnoe/openup_images_source_2014"
DESTINATION_IMAGE_DIR = "/home/nnoe/openup_images_dest_2014"
LOG_FILE = File.join(DESTINATION_IMAGE_DIR, "/openup_convert_log_2014.csv")

COP_IMAGE_DIR = File.join(DESTINATION_IMAGE_DIR, "/intermediate_copyright")
RES_IMAGE_DIR = File.join(DESTINATION_IMAGE_DIR , "/intermediate_resized")
TMP_TEXT_DIR = File.join(DESTINATION_IMAGE_DIR , "/tmp_text")
DEST_IMAGE_DIR = File.join(DESTINATION_IMAGE_DIR, "/finished")

BORDER_SIZE = 100
#FINAL_WIDTH = 450 # (we have to check it's acceptable for all pictures)
FINAL_WIDTH = 700

COPYRIGHT_BANNER_FILE = "./copyright.jpg"

SPACE_AROUND_SN = 20

FONT_FAMILY_SN = 'Verdana-Italic'
FONT_SIZE = 26

def write_layer_with_parents(layer, path)
  # Create parent directories if necessary...
  pa = path.split("/")
  pa.slice!(-1)
  FileUtils.mkdir_p(File.join(pa))
  #... and saves image
  layer.write(path)
end


# Script execution starts here
pictures = []

CSV.open(LOG_FILE, "w") do |csv|
  csv << ["filename", "processed", "interpreted_scientific_name"]
  
  # First, we parse the source hierarchy and we fill the picturess array with scientific name
  Find.find(SOURCE_IMAGE_DIR) do |f|
   csv_line = []
   csv_line[0] = f
    
   if f.match(/\.jpg\Z/) or f.match(/\.JPG\Z/) # name ends in .jpg
     filename = f.split("/").last
     filename_without_extension = filename.split(".").first
     
     # drop the last part to get the sn
     sn_array = filename_without_extension.split(" ")
     
     if sn_array.last != "copie" # General case, last part is the code...
      sn = sn_array[0...-1].join(' ')
     else # But sometimes, last part is 'copie' and the code is just before
      sn = sn_array[0...-2].join(' ')
     end
     
     pictures << {:filename => f.gsub(SOURCE_IMAGE_DIR, ""), :sn => sn }

     csv_line[1] = 'true'
     csv_line[2] = sn
    else
      csv_line[1] = 'false'
    end
    
    csv << csv_line
  end
  
end  
  
# Main loop
pictures.each do |entry|
  img = Image.read(File.join(SOURCE_IMAGE_DIR, entry[:filename]))
  layer = img[0] # no anim nor multi layer file
  
  # Resize
  scale_factor = (FINAL_WIDTH + 0.0 - (2*BORDER_SIZE)) / layer.columns
  layer.resize!(scale_factor)
  
  # Add border
  layer.border!(BORDER_SIZE, BORDER_SIZE, 'white')
  
  resized_path = File.join(RES_IMAGE_DIR, entry[:filename])
  write_layer_with_parents(layer, resized_path)
  layer.destroy! # To free memory
  
  # Add RBINS logo + copyright mention
  assembly = ImageList.new(resized_path, COPYRIGHT_BANNER_FILE,)
  layer = assembly.append(true)
  resized_with_copyright_path = File.join(COP_IMAGE_DIR, entry[:filename])
  write_layer_with_parents(layer, resized_with_copyright_path)
  
  sn_block = render_cropped_text(entry[:sn], FINAL_WIDTH, 100) do |img|
    img.font = FONT_FAMILY_SN
    img.background_color = '#CCC'
    img.pointsize = FONT_SIZE
    img.gravity = Magick::NorthGravity
    img.fill = 'black'
    #img.font_style = Magick::ItalicStyle
  end
  
  # Add 2 small borders (over and under sn), to make it less cramped
  sn_block = sn_block.extent(sn_block.columns, sn_block.rows + SPACE_AROUND_SN, 0, -SPACE_AROUND_SN)
  sn_block = sn_block.extent(sn_block.columns, sn_block.rows + SPACE_AROUND_SN)
  
  tmp_text_path = File.join(TMP_TEXT_DIR, entry[:filename])
  write_layer_with_parents(sn_block, tmp_text_path)
  
  assembly2 = ImageList.new(tmp_text_path, resized_with_copyright_path)
  layer = assembly2.append(true);
    
    
  write_layer_with_parents(layer, File.join(DEST_IMAGE_DIR, entry[:filename]))
  
  GC.start # ... or rmagick leaks will eat all memory
end


