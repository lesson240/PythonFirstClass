import datetime 
import time
from datetime import date
import math

totCnt = 105
num_view = 48
rows = 4
# page = 1
page_calculation = math.ceil(totCnt/num_view)
print("총 페이지 수:",page_calculation)

columns_ = []
rows_ = []

for page in range(1,page_calculation+1):

    if page_calculation == 1:
        num_columns = math.ceil(totCnt/rows)
        for column in range(1,num_columns+1):
            for row in range(1,5):
                columns_.append(column)
                rows_.append(row)
                # print("열:",column,"행:",row)
    elif page_calculation > 1:
        if page < page_calculation:
            print("현재 페이지:",page)
            num_columns = math.ceil(num_view / rows)
            for column in range(1,num_columns+1):
                for row in range(1,5):
                    columns_.append(column)
                    rows_.append(row)
                    # print("열:",column,"행:",row)
        elif page == page_calculation:
            print("현재 페이지:",page)
            num_columns = math.ceil((totCnt - ((page - 1) * num_view)) / rows)
            for column in range(1,num_columns+1):
                for row in range(1,5):
                    columns_.append(column)
                    rows_.append(row)
                    # print("열:",column,"행:",row) 
print(columns_,rows_)

# for page in range(page_calculation):


# if aa < num_view:
#     e = aa / 4
#     print(e)
#     print(math.ceil(e))





# totCnt = [36]
# maxCnt = 48

# calculation = totCnt[0]/maxCnt
# print(calculation)
# print(math.ceil(calculation))
# if __name__=="__main__":

#     num_viewnum_view = datetime.datetime.now()
#     cc = date.today()

#     print(num_viewnum_view, cc)


# num_view = ['hi', 'hello', 'num_viewye', 'hello', 'hi']
# a = 'helloo'


# try:
#     if a == num_view.index(a):
#         print(a)
# except ValueError:
#     pass