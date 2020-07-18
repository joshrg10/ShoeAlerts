from bs4 import BeautifulSoup
import requests
import csv
import smtplib, ssl

# url = "https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw=allen%20edmonds&_sacat=0&rt=nc&_udhi=20"


def findNewResults(search_name, link):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
    req = requests.get(link, headers)
    soup = BeautifulSoup(req.content, 'html.parser')

    def getNumberOfResults(html):
        number_of_results_section = html.findAll("h1", {"class": "srp-controls__count-heading"})
        split = 'class="BOLD">'
        number_of_results = int(str(number_of_results_section).split(split)[1].split("<")[0].replace(",", ""))  # Get number of search results
        return number_of_results

    def getResults(number_of_search_results, html):
        results = []
        for x in range(number_of_search_results):
            results_section = html.find("li", {
                "data-view": "mi:1686|iid:" + str(x + 1)})  # Todo change "1" to iteration in for loop
            link = results_section.find(href=True)['href']
            results.append(link)
        return results

    def writeNewResultsToCsv(filename):
        with open(filename + '.csv', "w") as outfile:
            for entries in results_links:
                outfile.write(entries)
                outfile.write("\n")

    def compareSearchResults(search_name, new_search_links):
        try:
            csv_file = str(search_name) + ".csv"
            with open(csv_file, newline='') as f:
                reader = csv.reader(f)
                data = list(reader)

            last_search_results = []
            for x in range(len(data)):
                result = data[x]
                last_search_results.append(str(result))

            new_items = []
            for x, i, in enumerate(new_search_links):
                if str(i) not in str(last_search_results):
                    new_items.append(i)
            print("new items " + str(new_items))

            if new_items == []:
                return True
            else:
                new_results = []
                for x in range(len(new_search_links)):
                    if str(new_search_links[x]) in str(last_search_results):
                        pass
                    else:
                        new_results.append(new_search_links[x])
                if len(new_results) > 0:
                    return new_results
                else:
                    return True
        except:
            with open(search_name + '.csv', "w") as outfile:
                for entries in results_links:
                    outfile.write(entries)
                    outfile.write("\n")
            print("New File Created: " + str(search_name) + ".csv")
            return new_search_links

    def sendNewResultsViaEmail(new_results_for_email):
        username = 'jrgray2k20@gmail.com'
        password = "5}jn,(8T#nvC`{B="
        recipient = 'josh.readfern@gmail.com'

        # Create Email Message
        message_list = ""
        for x, i in enumerate(new_results_for_email):
            message_list = message_list + "\n" + str(x + 1) + ". " + str(i)

        subject = "New " + search_name + " Results"
        text = " You have " + str(len(new_results_for_email)) + " new result(s): " + message_list
        message = 'Subject: {}\n\n{}'.format(subject, text)

        # Send Email
        with smtplib.SMTP('smtp.gmail.com:587') as s:
            s.starttls()
            s.login(username, password)
            s.sendmail(username, recipient, msg=message)
            s.quit()

    results_number = getNumberOfResults(html=soup)
    results_links = getResults(number_of_search_results=results_number, html=soup)
    comparison_result = compareSearchResults(search_name=search_name, new_search_links=results_links)
    if comparison_result is str:
        print("running comparison again...")
        compareSearchResults(search_name=search_name, new_search_links=results_links)
    if comparison_result == True:
        print("No new results")
    else:
        sendNewResultsViaEmail(new_results_for_email=comparison_result)
        number_of_new_results = len(comparison_result)
        print(str(number_of_new_results) + " new results")
        print(comparison_result)
        write_changes_confirmation = "Y"
        if write_changes_confirmation == "Y":
            writeNewResultsToCsv(filename=search_name)

# Create Dictionary of search name and link
with open('Searches.csv', mode='r') as infile:
    reader = csv.reader(infile)
    with open('temp.csv', mode='w') as outfile:
        writer = csv.writer(outfile)
        searches_dict = {rows[0]:rows[1] for rows in reader}


for x, i in enumerate(searches_dict):
    name = i
    url = searches_dict[i]
    findNewResults(search_name=name, link=url)

print("Complete")
