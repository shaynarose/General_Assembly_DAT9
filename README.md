## dat9_hw1

# 1) chipotle.tsv
* Columns are order ID, quantity, name, description, and price.  Each row is an item, which can be the entire order or part of the order.
* There are 1834 orders
* There are 4623 lines
* Chicken burritos are more popular than steak (553 vs. 386)
* Chicken burritos more often have black beans than pinto beans (282 vs. 105)

# 2) Dictionary occurs twice in Dat9

# 3) 
*I tried to find the number of times orders of only chips occured, aka without a main dish.  My thought process was to limit the code down to orders with only one line via sort and uniq and then pick out chips from that via a grep search.  But then I realized that doing this would only take out other line items in an order and show which orders included chips, not which orders included only chips.  It's something that sounds like an if statement, but I'm not sure how to do it in the command line.
