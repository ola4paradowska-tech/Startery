from Bio import Entrez
import pprint

Entrez.email = "ola4paradowska@gmail.com"

handle = Entrez.elink(
    dbfrom="gene",
    db="nucleotide",
    id="854916"
)

result = Entrez.read(handle)

pprint.pprint(result)