dict = {'a':'test', 'b':'test2'}
listzest = dict.keys()
print(list(listzest))
if 'testz' in dict.values() :
    print('omg')

input_csv_file_name='/Users/nguyen/Desktop/RS/data_source/tmdb_5000_movies.csv'
name = input_csv_file_name.split('/')[-1]
print(name)