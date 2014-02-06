The problem
===========

As described in the import descriptions, the current process is overly fragile and complex:

- Most data comes from the yellow columns of the source Excel file.
- The white columns contains incorrect data, coming from the photographer and WE CANNOT USE IT
- As no taxonomic informations are provided in the "yellow" columns, we have to extract it from the image filename and path (for family, subfamily, ...). Orgiginally André wrote a regexp to do so in walk.rb
- ... But the image transormation script (step 1) also needs the scientific name to incrust and (badly) reinvent this "taxonomic data extraction" in its first loop !!! Huge risk of inconsistencies.
- Given the fragility of this approach, they don't always follow their own nomenclature rules in filenames and it becomes impossible to parse them with regular expressions (yes, we tried to patch/improve/add code in walk.rb)
=> The main issue is that the taxonomic information cannot be extracted from the Excel file, and regexp-based reconciliation is really complex and fragile (or even impossible)
=> This can be even worse if they add much more images in the future, as intended.

What has been decided for the urgent 2014 update
================================================

- That we add new features and "planches" to the website, but we do not perform the import of the 200 new images.

Possible fix for later (not recommended)
========================================

- We continue with the old, complex approach but ask them to fix their recent filenames so they match the old regexp in walk.rb

Suggested long-term solution
============================

- The RBINS team should provide the complete data (full XLS file + complete image dir hierarchy) and not only "recent data to merge"
- Taxonomic data should be included in the XLS file and ignored in the filenames / filepaths
- That would allow to write a very simple script that start to extract once all the data from the Excel file and use it for all purposes:
    * Filling the OpenUP database (or at least the rbinsphotos view, the only necessary thing - just not forget rbinsmetadata).
    * Overlay scientific name in images at step 1.
- Julien has already started to work on this approach but had to stop when we realized we currently don't have CORRECT (yellow columns) data for it. Let's keep the code if we choose this option !
- As the RBINS team work manually, it would be a huge effort for them to just add all this missing data. We could help them by pre-filling the num columns using Andre's regexp in walk.rb for the easy cases. They would therefore only had to review this, add the data the regexp was not able to grasp (and of course to continue filling/curating these new columns)
- These new columns should be yellow :)
- Once this is done, we can suggest removing this info from the filenames and creating a flat directory for all images.
- We can show them advantages of this approach and maybe create a script or two to fulfill their needs (imageID to scientificname for example)
- To avoid confusion next time, I suggest renaming the not curated columns: "espèce" => "verbatimSpecies"
- Other possibilities to further improve data: show them to use different sheets to simulate RDBMS tables.
- Let's fix a meeting / work session soon for this.
