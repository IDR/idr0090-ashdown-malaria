FROM openjdk:8

RUN yum install -y wget unzip

RUN wget https://downloads.openmicroscopy.org/bio-formats/6.5.1/artifacts/bftools.zip && unzip bftools.zip && rm bftools.zip

RUN wget https://artifacts.openmicroscopy.org/artifactory/maven/idr/formats-api/0.6.4/formats-api-0.6.4.jar && mv formats-api-0.6.4.jar bftools/formats-api.jar
RUN wget https://artifacts.openmicroscopy.org/artifactory/maven/idr/formats-api/0.6.4/formats-api-0.6.4.jar && mv formats-bsd-0.6.4.jar bftools/formats-bsd.jar
RUN wget https://artifacts.openmicroscopy.org/artifactory/maven/idr/formats-api/0.6.4/formats-api-0.6.4.jar && mv formats-gpl-0.6.4.jar bftools/formats-gpl.jar

ENV BF_MAX_MEM 4g
ENTRYPOINT ["./bftools/bfconvert"]