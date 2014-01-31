@@total=@@passed=@@failed=0

ROOT_DIRECTORY = "/home/nnoe/openup_images_dest_2014/finished"

def image(family, subdir, filename)
  if filename=='.' or filename=='..'
    return
  end
  if File.file?(filename)
    @@total +=1
    re1 = Regexp.new('^(\w+)\s+(\(\w+\))?\s*?([\d\w-]+)\s*?(\w+)?\s*?(AT|HT|HT et|PT)?\s*?(\d+[.\d\w-]+)\s*?(\w+)?\s*?\.(\w+)$') 
#                       GENUS  (subgenus)   species        subspecies    AT/PT/HT       number copie .jpg/JPG 
    md = re1.match(filename)
    if !md.nil? 
      @@passed +=1
     puts "#{@@total};#{family};#{subdir};#{filename};#{md[1]};#{md[2]};#{md[3]};#{md[4]};#{md[5]};#{md[6]};#{md[7]};#{md[8]}\n"    
    else 
      puts "#{@@total};#{family};#{subdir};#{filename};;;;;;;;\n"    
      @@failed +=1
      
    end
  end
end

def family(family)
  if family=='.' or family=='..'
    return
  end
#  puts "Family: #{family}"
  Dir.chdir(family)
  files=Dir.glob('*')
  files.each(){|f|
    if File.file?(f)
      image(family, '', f)
    end
    if File.directory?(f)
      Dir.chdir(f)
      files2=Dir.glob('*')
      files2.each(){|ff|
        image(family, f, ff)
      }
      Dir.chdir('..')
    end    
  }
  Dir.chdir('..')
end


puts "Id;Family;Subdir;Filename;Genus;SubGenus;Species;SubSpecies;Extra;Image;Copie;Extension\n"    
Dir.chdir(ROOT_DIRECTORY)
d=Dir.open('.')
d.each(){|f|
  if File.directory?(f)
    family(f)
  end
}
#puts "Count=#{@@total},Failed=#{@@failed},Passed=#{@@passed}"