

print ("\nCategories:\n")

count = 0
for item in data[u'products_and_categories']:
    print(str(count)+' '+str(item))
    count+=1
choice = raw_input('What Catagory? (1-10)')
