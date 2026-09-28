|Issue   |Example   |Proposed Fix   |
|---|---|---|
|Several cols in listings.csv have no non-null entries   |Col 7 neighbourhood_overview   |Delete Them   |
|Price only has 62240 non-null rows   |   |Delete the null rows possibly? Not much we can do without price   |
|Price is a string and starts with "$"  |   |Change to float (or is there a "price" dtype?) and remove "$"   |
|Bathrooms in the form of "int + "baths"" or shared baths and also sometimes have a decimal    |1.5 shared baths    |Clip to only the number.   |
|Room type includes hotel rooms   |   |Take out hotel rooms as they are very likely not available to buy as an investment oppourtinity   |
|col "minimum_nights" has values into the thousands   |"1125.0"   |Remove those ones with minimum_nights above a certain threshold   |
|"first_review", "last_review" are strings   |   |Change to date   |
|"reviews_per_month" has around 20k null entries   |   |Remove them ?   |
|Following from earler: there is a "bathrooms" col with just a number but its 50% null. bathrooms text as more complete data even if its in form stated above   |   |use number-extracted from "bathrooms_text"   |
|   |   |   |
|   |   |   |