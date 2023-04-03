# Luiss - Management and Computer Science - Algorithm 2022/2023 
# Please fill the empty parts with your solution
from typing import Tuple, List, Dict
import heapq

def read_file(file_path: str) -> any:
    """
    This function reads the dataset containg all the information about the 
    cryptocurrecies. The information are stored in a .txt file.
    
    Parameters:
    :file_path: The current path where the file you want to read is located
    
    @return: A data structure contining the information of the crypto
    """
    
    with open(file_path, "r") as file:
        dictionary = dict()
        for line in file.readlines():
            line.split(",")
            element = line.rstrip().split(',')
            if element[0] in dictionary:
                dictionary[element[0]].append(element[1:])
            else:
                dictionary[element[0]]=[element[1:]]
        return dictionary
    

def crypto_stats(data, crypto_name: str, interval: Tuple[int, int]) -> Tuple[float, float, float]:
    """
    This function calculates the minimum, average, and maximum price values of a crypto
    whose name is passed in input within a specific period of time [a,b] passed
    in input. Notice that [a,b] can be an interval that might exceed the actual monitoring
    time of the crypto given in input.
    
    If any error occurs, return the default value (0.0, 0.0, 0.0)
    
    Parameters:
    :data: The data structure used to calculate the statistics
    :crypto_name: The name of the cryptocurrency to calculate statistics for
    :interval: The time interval consisting of a tuple of two values (a,b)
    
    @return: A tuple that contains the minimum, average, and maximum price values
    """
    all_data = read_file(data)
    filtered_data = []

    try:
        for values in all_data[crypto_name]:
            if float(values[0]) >= interval[0] and float(values[0]) <= interval[1]:
                filtered_data.append(float(values[1]))

        minimum = min(filtered_data)
        maximum = max(filtered_data)
        average = sum(filtered_data) / len(filtered_data)
        
        return (minimum, average, maximum)

    except Exception:
        return (0.0, 0.0, 0.0)


def sort_data(data) -> List[Tuple[str, float]]:
    """
    This function sorts the cryptocurrencies first in alphabetical order, and,
    then, for each of them, it performs a sort according to the day of monitoring.
    
    It is forbidden to use any kind of libraries such as Pandas, or functions like
    list.sort()!
    
    Parameters:
    :data: A data structure containing all the information about the cryptos
    
    @return: A sorted list of tuples containing (crypto name, price)
    """
    all_data = read_file(data)
    all_keys = [key for key in all_data.keys()]
    sorted_data = []

    for i in range(0, len(all_keys)):
        for j in range(0, len(all_keys)):
            if all_keys[i] < all_keys[j]:
                temp = all_keys[i]
                all_keys[i] = all_keys[j]
                all_keys[j] = temp

    def mergeSort(arr):
        if len(arr) > 1:
            mid = len(arr) // 2
            left = arr[:mid]
            right = arr[mid:]
            mergeSort(left)
            mergeSort(right)
        
            i = j = k = 0
            while i < len(left) and j < len(right):
                if left[i] < right[j]:
                    arr[k] = left[i]
                    i += 1
                else:
                    arr[k] = right[j]
                    j += 1
                k += 1
            
            while i < len(left):
                arr[k] = left[i]
                i += 1
                k += 1
            
            while j < len(right):
                arr[k] = right[j]
                j += 1
                k += 1
        return arr
    
    for k in all_keys:
        raw = {int(elem[0]):float(elem[1]) for elem in all_data[k]}
        sorted_days = mergeSort(list(raw.keys()))
        for day in sorted_days:
            price = raw[day]
            sorted_data.append((k, price))
    return sorted_data
        

def get_max_value(data, crypto: str, month: int) -> Tuple[int, float]:
    """
    This function must return the maximum price for a given crypto in
    a specific month.
    
    Parameters:
    
    :data: A data structure containing the information about the cryptos.
    :crypto: The crypto for which to search the maximum value.
    :month: The month in which to search for the maximum value.
    
    Assumption: each month contains 30 days. Notice that the month can be
    a natural number in [1,inf). Example the 13th month represents the first
    month of the second year of monitoring; the 14th month represents the
    second month of the second year of monitoring, and so on.
    
    @return: A tuple containing the day in which the crypto reached the maximum price,
             along with the maximum value for that crypto
    """

    def partition(list, low, high):
        i = low
        pivot = list[high]

        for j in range(low, high):
            if list[j] <= pivot:
                list[i], list[j] =  list[j], list[i]
                i += 1

        list[i], list[high] = list[high] ,list[i]

        return i
        

    def quick_sort(list, low, high):
        if low < high:
            partition_index = partition(list, low, high)
            quick_sort(list, low, partition_index - 1)
            quick_sort(list, partition_index + 1, high)
        

    all_data = sort_data(data)
    dictionary = dict()
    day = 0

    try:
        for elem in all_data:
            if elem[0] == crypto:
                day += 1
                if day <= 30 and month == 1 or (month * 30) - 29  <= day <= (month * 30):
                    dictionary[day] = elem[1]

        keys = list(dictionary.keys())

        #We need an unsorted list of prices because we are getting the day_of_max price by the index of the max price and quicksort modifies the list without considering the keys.
        prices_unsorted = list(dictionary.values())
        prices_sorted = list(dictionary.values())
        quick_sort(prices_sorted, 0, len(prices_sorted) - 1)
        
        max_price = prices_sorted[len(prices_sorted) - 1]
        day_of_max_price = keys[prices_unsorted.index(max_price)]

        return tuple((day_of_max_price, max_price))

    except Exception:
        return tuple((-1, -1))
    
        
print(get_max_value("data/dataset_full.txt", "polygon", 5))



def search(data, value: float, crypto: str) -> Tuple[int, float]:
    """
    This function searches for a specific price in a given data series and
    returns a tuple with the day and the price for a given cryptocurrency.
    If the searched value is not present in the data, the function returns the
    closest price. It compares two values of the data series, one at position i
    and the other at position j, and returns the price closest to the searched value.
    
    N.B.: If you have more than one possible day whose corresponding price is closest
    to the value in input, return the minimum day.
    
    Parameters:
    :data: A data structure that contains the value of price and volume of all cryptos.
    :value: The price value to be searched in the data.
    :crypto: The crypto name to search the value for.
    
    @return: A tuple containing the day on which the cryptocurrency reached the closest price
             and the closest price.
    """

    # TODO: Implement here your solution


    return (None, None)


def min_correlation_pathways(data,
                             crypto: str,
                             interval: Tuple[int,int]) -> Dict[str, List[str]]:
    """
    This function builds a minimal correlation pathways tree on the given
    data structure for a specific cryptocurrency in a designated temporal
    period. For each node x, the sum of the weights in the path from the root
    to x must be minimal.
    
    Parameters:
    :data: A data structure that contains the information of all cryptos.
    :crypto: The crypto name for which to build the tree.
    :interval: The temporal period for which to build the tree.
               It's in the form [x,y] where x is the beginning time and y is the end
               time.
               
    @return: The minimal correlation pathways tree
    """
    # TODO: Implement here your solution
    
    return None


def correlated_cryptos_at_lvl_k(data,
                                crypto: str,
                                level: int,
                                interval: Tuple[int,int]) -> List[str]:
    """
    This function retrieves the cryptocurrencies related to the one given in input
    at a particular level of correlation in a designated temporal period [x,y].
    
    Parameters:
    :data: A data structure that contains the information of all cryptos.
    :crypto: The crypto name to search correlations for.
    :level: The level at which the correlated cryptos should stand at.
    :interval: The temporal period for which to build the correlation tree.
               It's in the form [x,y] where x is the beginning time and y is the end
               time.
               
    @return: A list of cryptocurrencies
    """
    # TODO: Implement here your solution
    return None