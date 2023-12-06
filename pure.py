import csv, os


class ConvertCsv:
    def __init__(self):
        self.__location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__))
        )
        self.table = []

    def csv_to_table(self, file_name):
        self.table = []
        with open(os.path.join(self.__location__, file_name)) as f:
            rows = csv.DictReader(f)
            for r in rows:
                self.table.append(dict(r))
        return self.table


class DB:
    def __init__(self):
        self.database = []

    def insert(self, table):
        self.database.append(table)

    def search(self, table_name):
        for table in self.database:
            if table.table_name == table_name:
                return table
        return None


import copy


class Table:
    def __init__(self, table_name, table):
        self.table_name = table_name
        self.table = table

    def join(self, other_table, common_key):
        joined_table = Table(self.table_name + '_joins_' + other_table.table_name, [])
        for item1 in self.table:
            for item2 in other_table.table:
                if item1[common_key] == item2[common_key]:
                    dict1 = copy.deepcopy(item1)
                    dict2 = copy.deepcopy(item2)
                    dict1.update(dict2)
                    joined_table.table.append(dict1)
        return joined_table

    def filter(self, condition):
        filtered_table = Table(self.table_name + '_filtered', [])
        for item1 in self.table:
            if condition(item1):
                filtered_table.table.append(item1)
        return filtered_table

    def __is_float(self, element):
        if element is None:
            return False
        try:
            float(element)
            return True
        except ValueError:
            return False

    def aggregate(self, function, aggregation_key):
        temps = []
        for item1 in self.table:
            if self.__is_float(item1[aggregation_key]):
                temps.append(float(item1[aggregation_key]))
            else:
                temps.append(item1[aggregation_key])
        return function(temps)

    def select(self, attributes_list):
        temps = []
        for item1 in self.table:
            dict_temp = {}
            for key in item1:
                if key in attributes_list:
                    dict_temp[key] = item1[key]
            temps.append(dict_temp)
        return temps

    def pivot_table(self, keys_to_pivot_list, keys_to_aggreagte_list, aggregate_func_list):

        unique_values_list = []
        for key_item in keys_to_pivot_list:
            temp = []
            for dict in self.table:
                if dict[key_item] not in temp:
                    temp.append(dict[key_item])
            unique_values_list.append(temp)

        # combination of unique value lists
        import combination_gen
        comb_list = combination_gen.gen_comb_list(unique_values_list)

        pivot_table = []
        # filter each combination
        for item in comb_list:
            temp_filter_table = self
            for i in range(len(item)):
                temp_filter_table = temp_filter_table.filter(lambda x: x[keys_to_pivot_list[i]] == item[i])

            # aggregate over the filtered table
            aggregate_val_list = []
            for i in range(len(keys_to_aggreagte_list)):
                aggregate_val = temp_filter_table.aggregate(aggregate_func_list[i], keys_to_aggreagte_list[i])
                aggregate_val_list.append(aggregate_val)
            pivot_table.append([item, aggregate_val_list])
        return pivot_table

    def insert_row(self, dict1):
        self.table.append(dict1)

    def update_row(self, primary_attribute, primary_attribute_value,
                   update_attribute, update_value):
        # get the index
        index = ""
        for i in self.table:
            if i[primary_attribute] == primary_attribute_value:
                index = self.table.index(i)
        self.table[index][update_attribute] = update_value

    def __str__(self):
        return self.table_name + ':' + str(self.table)


converter = ConvertCsv()
my_DB = DB()
table1 = Table('movies', converter.csv_to_table('movies.csv'))
my_DB.insert(table1)
# Find the average value of ‘Worldwide Gross’ for ‘Comedy’ movies
table2 = table1.filter(lambda x: x['Genre'] == 'Comedy')
total_gross = table2.aggregate(lambda x: sum(x), 'Worldwide Gross')
avg_gross = table2.aggregate(lambda x: total_gross / len(x), 'Film')
print(f'The average value of "Worldwide Gross" for "Comedy" movies is {avg_gross}')

# Find the minimum ‘Audience score %’ for ‘Drama’ movies
min_score = table1.filter(lambda x: x['Genre'] == 'Drama').aggregate(lambda x: min(x), 'Audience score %')
print(f'The minimum "Audience score" % for "Drama" movies is {min_score}')

# count the number of fantasy movies
num_fantasy = table1.filter(lambda x: x['Genre'] == 'Fantasy').aggregate(lambda x: len(x), 'Genre')
print(f'The number of fantasy movies is {num_fantasy}')

# insert movie
dict = {}
dict['Film'] = 'The Shape of Water'
dict['Genre'] = 'Fantasy'
dict['Lead Studio'] = 'Fox'
dict['Audience score %'] = '72'
dict['Profitability'] = '9.765'
dict['Rotten Tomatoes %'] = '92'
dict['Worldwide Gross'] = '195.3'
dict['Year'] = '2017'
my_DB.search('movies').insert_row(dict)

# count again
num_fantasy = table1.filter(lambda x: x['Genre'] == 'Fantasy').aggregate(lambda x: len(x), 'Genre')
print(f'The number of fantasy movies is now {num_fantasy}')

# serious man update the  'Year' for the  'Film' :  'A Serious Man' to '2022'
my_DB.search('movies').update_row('Film', 'A Serious Man', 'Year', 2022)