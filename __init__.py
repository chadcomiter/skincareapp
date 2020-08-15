def solve(s):
    ##split the list via list(s)
    split = list(s)
    ##find the index where the character = " "
    indexes = []
    for i in split:
        if i == " ":
            indexes.append(i)
    ##remove the spaces from the original list
    def remove_vals_from_list(list, val):
        return [value for value in list if value != val]
    
    cleaned = remove_vals_from_list(split, " ")
    
    reversed = cleaned[::-1]
    ##Insert " " at the relevant indexes
    for i in indexes:
        reversed.insert(reversed[i], " ")
    
    output = ''
    return output.join(reversed)