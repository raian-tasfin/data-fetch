from bs4 import BeautifulSoup
import requests
import xlsxwriter

# get row data from a products url
def getProductData(url):
	productInformation = []

	productPage = requests.get(url);

	productSoup = BeautifulSoup(productPage.content,"html.parser")
	
	table = productSoup.find("table", {"class":"shop_attributes"})	
	if(not table):
		return []

	tableRows =  list(table.children)

	for i in tableRows:
		nameRow = list(i.children)
		nameRowData = list(nameRow[1].children)
		p = nameRowData[0]
		name = p.get_text()
		productInformation.append(name)

	# get blurb
	descriptionElement = productSoup.find("div", {"class" : "woocommerce-product-details__short-description"})
	p = list(descriptionElement.children)[0]
	productInformation.append(p.get_text())	

	return productInformation

# Web page urls
pageUrlList = []
# product urls
productUrlList = []
# list of product data lists
productDataList = []

# web page url count
urlCount = 0
productUrlCount = 0

# Generate web page urls
print("Generating Web Page URLs")
for i in range(1,6):
	tmp = "https://www.ikrimikri.com/shop/page/"+str(i)+"/"
	print(tmp)
	i+=1;
	pageUrlList.append(tmp)
# END Generate web page urls
print("URLs genrated: %d" % (1))
print("Complete")
print()

# Get product urls from each page
print("Listing product URLs from each page:")
for pageUrl in pageUrlList:
	
	print("Requesting page: %s" % (pageUrl))
	page = requests.get(pageUrl)
	
	print("Making soup")
	soup = BeautifulSoup(page.content,"html.parser")
	ul = soup.find("ul", {"class": "products columns-3"})
	productsOnPage = list(ul.children)

	print("Fetching URLs of Each Product")
	for product in productsOnPage:
		productChildList = list(product.children)
		a = productChildList[1]
		
		print("URL: %s" % (a.get('href')) )
		productUrlList.append(a.get('href'))
		productUrlCount+=1
	
	# END Get product urls from each page
	print("Product URLs fetched %d" % (productUrlCount))
	print("Complete")

print()

totalProductUrlCount = productUrlCount

print("Extracting product data from each url")
# Get product data from each product url
for productUrl in productUrlList:
	print("URL %s" % (productUrl) )
	productData = getProductData(productUrl)
	productDataList.append(productData)
	print("complete")
	productUrlCount-=1
	print("Extraction Remaining %d of %d" % ( productUrlCount, totalProductUrlCount ))
print("Extraction complete")	
print()

print("Opening workbook")
workbook = xlsxwriter.Workbook('data.xlsx')
worksheet = workbook.add_worksheet()

row = 1

productUrlCount = totalProductUrlCount

print("writing data to xlsx file")
for productInfo in productDataList:
	if(productInfo != []):
		print(productInfo[0])
		i=1
		for product in productInfo:
			worksheet.write(row, i, product)
			i+=1
		row+=1
		print("done")
		productUrlCount-=1
		print("remaining %d of %d " % (productUrlCount, totalProductUrlCount))

print("Complete")
print("closing workbook")

workbook.close()

print("complete")
# name writer illustrator isbn prize date page blurb
