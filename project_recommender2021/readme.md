How to run the project:
1) Install all the required python modules (django, sklearn, etc..)
2) go to the metadatageneration folder and paste your extracted jsons from here  https://drive.google.com/file/d/1je77e0Lq8naVUsjoOzk5RuI2H3ceHlSz/view into the folder 'extracted_jsons'
3) run the genearteCSV method
4) Go to the 'recommendation' folder and paste the ml-25m-dataset into the 'ml-25m' folder.
5) Copy and paste the custom_metadata.csv file generated in step 3 into the 'ml-25m' folder.
6) run the 'summary_similarity_preprocessing' file (this creates the TFIDF cosine similarity matrix to use for the summary similarity)
7) Run the django project

WARNING: Step 2 and 6 may take some time to finish!
