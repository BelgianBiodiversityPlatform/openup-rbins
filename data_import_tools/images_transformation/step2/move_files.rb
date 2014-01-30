require "rubygems"
require "active_record"
require "fileutils"

SOURCE_FOLDER = "/home/nnoe/openup_images_dest/transformed_images"
SOURCE_ONLY_PICTURE_FOLDER = "/home/nnoe/openup_images_dest/intermediate_resized"

# These two folders should exists prior running this script
DEST_FOLDER = "/home/nnoe/openup_images_apache"    
DEST_FOLDER_ONLY_PICTURES = "/home/nnoe/openup_images_apache/pictures_only"

#Change this to reflect your database settings
ActiveRecord::Base.establish_connection (
  {:adapter => 'postgresql', :host => "dev",
  :username => "nnoe",
  :password => "jvk4QNHB",
  :database => "openup_rbins"})

#Now define your classes from the database as always
class Rbinsphotos < ActiveRecord::Base
  #blah, blah, blah
end

#Now do stuff with it
lines = Rbinsphotos.find :all

lines.each do |l|
  begin
    #puts "passe"
    #puts l.origpathname
    source_path = File.join(SOURCE_FOLDER, l.origpathname)
    FileUtils.copy(source_path, File.join(DEST_FOLDER, "#{l.unitid}.jpg"))
    
    source_path_only_pictures = File.join(SOURCE_ONLY_PICTURE_FOLDER, l.origpathname)
    FileUtils.copy(source_path_only_pictures, File.join(DEST_FOLDER_ONLY_PICTURES, "#{l.unitid}.jpg"))
  rescue
    puts "Error during copy: unitid=#{l.unitid} source_path=#{source_path}"
  end
end
