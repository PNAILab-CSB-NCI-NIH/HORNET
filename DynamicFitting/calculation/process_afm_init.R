## process AFM data obtained from experiment and calibration to apply to CafeMol calculation
## Usage: Rscript process_afm_init.R afm.txt 
## afm.txt is the AFM data file in Angstroms unit
## the output will be an input file (.inp) for cafemol

#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)
#print(args[1])
#length(args)
## test if there is at least one argument: if not, return an error
if (length(args) != 1) {
  stop("Please provide afm data file", call.=FALSE)
}

#install.packages("dplyr")
library(dplyr)

afm.file = args[1]
d = read.table(afm.file, 
               sep="", 
               fill=FALSE, 
               strip.white=TRUE)

# min(d$V3) 
d$V3 = d$V3 - min(d$V3)
# min(d$V3)
# dim(d)
df.new = d
# dim(df.new)
# get every 5th row
#df.new = df[seq(1, nrow(df), 5), ]
df.new$V1 = round(df.new$V1*10, digits = 1)
df.new$V2 = round(df.new$V2*10, digits = 1)
## offset x and y pixel position
df.new$V1 = df.new$V1 - min(df.new$V1) + 5
df.new$V2 = df.new$V2 - min(df.new$V2) + 5
# min(df.new$V1)
# min(df.new$V2)

## set z values less than 1A to zero
V3.sparse = df.new$V3*10
V3.sparse[V3.sparse < 1.0] = 0.000

df.new$V1 = format(df.new$V1, digits = 1, nsmall = 1)
df.new$V2 = format(df.new$V2, digits = 1, nsmall = 1)
df.new$V3 = format(round(V3.sparse, digits = 3))


# head(df.new)
# dim(df.new)
## get unique combination of x y pixel position
df.new.unique = df.new[!duplicated(df.new[1:2]),]
# View(df.new.unique)
# dim(df.new.unique)

out.file = paste0(tools::file_path_sans_ext(basename(afm.file)),"_init.txt")
if (file.exists(out.file)) 
  #Delete file if it exists
  file.remove(out.file)
write.table(df.new, out.file, 
            sep = " ", quote = FALSE, row.names = FALSE, col.names = FALSE, append = FALSE)

