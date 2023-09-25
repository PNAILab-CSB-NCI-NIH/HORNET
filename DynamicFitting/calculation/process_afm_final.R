## process AFM data obtained from experiment and calibration to apply to CafeMol calculation
## Usage: Rscript process_afm_data.R afm.txt dimer_template.txt
## afm.txt is the AFM data file in Angstroms unit, dimer_template.txt is a template header file
## the output will be an input file (.inp) for cafemol

#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)
#print(args[1])
#length(args)
## test if there is at least one argument: if not, return an error
if (length(args) != 2) {
  stop("Please provide afm data file and template header file", call.=FALSE)
}

#install.packages("dplyr")
library(dplyr)

afm.file = args[1]
# afm.file = "padded_cmpt1_1A_rot_init.txt"
d = read.table(afm.file, sep=" ", 
               fill=FALSE, 
               strip.white=TRUE)
# head(d)
# min(d$V3) 
d$id = rep("AFM_IMAGE", nrow(d))
#move last column to first
df.new <- d %>%   select(id, everything())
df.new$V3[df.new$V3 < 1.0] = 0.000

df.new$V1 = format(df.new$V1, digits = 1, nsmall = 1)
df.new$V2 = format(df.new$V2, digits = 1, nsmall = 1)
df.new$V3 = format(round(df.new$V3, digits = 3))

#### Generate the input file
header.file = args[2]
top_part = readLines(header.file)

out.file = "cafe_input.inp"
if (file.exists(out.file)) 
  #Delete file if it exists
  file.remove(out.file)

writeLines(top_part, out.file)
write.table(df.new, out.file, 
            sep = " ", quote = FALSE, row.names = FALSE, col.names = FALSE, append = TRUE)
write(">>>>", out.file, append = TRUE)

