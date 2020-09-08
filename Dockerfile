FROM openjdk:8

RUN apt-get update && apt-get install -y wget unzip

RUN wget https://downloads.openmicroscopy.org/bio-formats/6.5.1/artifacts/bftools.zip && unzip bftools.zip && rm bftools.zip
RUN wget https://artifacts.openmicroscopy.org/artifactory/maven/idr/bioformats_package/0.6.4/bioformats_package-0.6.4.jar && mv bioformats_package-0.6.4.jar bftools/bioformats_package.jar

ENV BF_MAX_MEM 4g
ENTRYPOINT ["./bftools/bfconvert"]