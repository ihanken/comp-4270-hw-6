from random import *
import operator
from texttable import Texttable

class Page():
    ''' Initializers '''
    # Fully explicit initializer
    def __init__(self, pageNumber, timeLoaded = -1, lastRef = -1, m = -1, r = -1):
        self.__pageNumber = pageNumber
        self.__timeLoaded = timeLoaded if timeLoaded >= 0 else randint(1, 500)
        self.__lastReference = lastRef if lastRef >= 0 else randint(501, 1000)
        self.__modified = m if m >= 0 else getrandbits(1)
        self.__reference = r if r >= 0 else getrandbits(1)
        self.__nruClass = 2 * self.__reference + self.__modified

    ''' Getters '''
    @property # Page.pageNumber
    def pageNumber(self): return self.__pageNumber

    @property # Page.timeLoaded
    def timeLoaded(self): return self.__timeLoaded

    @property # Page.lastReference
    def lastReference(self): return self.__lastReference

    @property # Page.modified
    def modified(self): return self.__modified

    @property # Page.reference
    def reference(self): return self.__reference

    @property # Page.nruClass
    def nruClass(self): return self.__nruClass

    def __repr__(self): return "Page()" # Non-verbose printing.

    def __str__(self): # Verbose printing
        tt = Texttable() # Instantiate a text table.

        tt.set_cols_align(["c", "c", "c", "c", "c"]) # Set column alignment.
        tt.set_cols_valign(["m", "m", "m", "m", "m"]) # Set row alignment.

        tt.add_rows([
            ["Page Number", "Time Loaded", "Last Reference", "M", "R"], # Title
            [
                self._pageNumber,       # Page #
                self._timeLoaded,       # Time Loaded
                self._lastReference,    # Time Last Referenced
                self._modified,         # M Bit
                self._reference         # R Bit
            ]
        ])

        return tt.draw() # Return the table as a string.

'''
NRU Algorithm

In the Not Recently Used Algorithm, the operating system divides pages into 4
classes:

3. referenced, modified
2. referenced, not modified
1. not referenced, modified
0. not referenced, not modified

The lower classes have higher priority to be removed. So the lowest class found
is chosen and then a random page from this class is chosen.

This function
'''
def getNRUReplacement(pages, lowestNRUClass):
    # Filter the list to only include pages of the lowest NRU class.
    lowestNRUPages = [page for page in pages if page.nruClass == lowestNRUClass]

    # Print the result.
    print("a. Page {} is replaced when using the NRU algorithm."
            .format(choice(lowestNRUPages).pageNumber))

'''
FIFO Replacement

The First-In First-Out algorithm chooses the page loaded least recently and
replaces that page.

This function sorts by the time loaded and then chooses the page at the
beginning of the list.
'''
def getFIFOReplacement(pages):
    # Sort the list by time loaded.
    pagesByLoad = sorted(pages, key=operator.attrgetter('timeLoaded'))

    # Print the result.
    print("b. Page {} is replaced when using the FIFO algorithm."
            .format(pagesByLoad[0].pageNumber))

'''
LRU Replacement

The Least Recently Used algorithm chooses the page referenced least recently and
replaces that page.

This function sorts by the time last referenced and then chooses the page at
the beginning of the list.
'''
def getLRUReplacement(pages):
    # sort the list by time last referenced.
    pagesByReference = sorted(pages, key=operator.attrgetter('lastReference'))

    # Print the result.
    print("c. Page {} is replaced when using the LRU algorithm."
            .format(pagesByReference[0].pageNumber))

'''
Second Chance Replacement

The Second Chance Replacement algorithm is an improvement on the FIFO algorithm.
The algorithm still chooses a page to replace based on the time it was loaded
at, but it checks each reference bit, and if the reference bit is set to 1, it
changes the reference bit to 0, moves the page to the back of the queue, and
moves on. If the reference bit is 0, that page is chosen to be replaced.

This function simply looks for the first page with a reference bit set to 0. If
none are found, it chooses the first page in the list.
'''
def getSecondChanceReplacement(pages):
    # Sort the list by time loaded.
    pagesByLoad = sorted(pages, key=operator.attrgetter('timeLoaded'))

    pageLastReferenced = None # Instantiate the page to replace as None.

    for page in pagesByLoad: # Iterate through each page.
        if page.reference == 0: # If a reference bit of 0 is found,
            pageLastReferenced = page # choose this page to be replaced.
            break # Break out of the loop.

    # If there was no page with a 0 referene bit found, use the first page
    # based on time loaded.
    if not pageLastReferenced: pageLastReferenced = pagesByLoad[0]

    # Print the result.
    print("d. Page {} is replaced when using the Second Chance Algorithm."
            .format(pageLastReferenced.pageNumber))

def printResults(useRandomValues):
    pages = [] # Our page record.

    lowestNRUClass = 3 # Instantiate lowest class to the highest class possible.

    if not useRandomValues: # Use the static values.
        print("\n1. Here is the table with the static values and the results.\n")

        page = Page(0, 126, 280, 1, 0)  # Generate page 0.
        pages.append(page)              # Add the page to our record.

        page = Page(1, 230, 265, 0, 1)  # Generate page 1.
        pages.append(page)              # Add the page to our record.

        page = Page(2, 140, 270, 0, 0)  # Generate page 2.
        pages.append(page)              # Add the page to our record.

        page = Page(3, 110, 285, 1, 1)  # Generate page 3.
        pages.append(page)              # Add the page to our record.

        # Get lowestNRUClass
        lowestNRUClass = min([page.nruClass for page in pages])
    else: # Use the random values.
        print("\n2. Here is the table with random values and the results.\n")

        for i in range(4):      # Iterate 4 times.
            page = Page(i)      # Generate a page with random values.
            pages.append(page)  # Add the page to our record.

            # Update lowestNRUClass
            lowestNRUClass = min(lowestNRUClass, page.nruClass)

    tt = Texttable() # Instantiate our text table.

    tt.set_cols_align(["c", "c", "c", "c", "c"])    # Set column alignment.
    tt.set_cols_valign(["m", "m", "m", "m", "m"])   # Set row alignment

    # Add rows to our table.
    tt.add_rows([["Page Number", "Time Loaded", "Last Reference", "M", "R"]]
                + [[ # Create a row for each page.
                      page.pageNumber,
                      page.timeLoaded,
                      page.lastReference,
                      page.modified,
                      page.reference
                  ] for page in pages])

    print(tt.draw()) # Print the table.
    print() # Print a blank line.

    getNRUReplacement(pages, lowestNRUClass)    # Print NRU result.
    getFIFOReplacement(pages)                   # Print FIFO result.
    getLRUReplacement(pages)                    # Print LRU result.
    getSecondChanceReplacement(pages)           # Print Second Chance result.

if __name__ == "__main__":
    printResults(False) # Static values.
    printResults(True)  # Random values.
