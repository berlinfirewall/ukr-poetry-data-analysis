import matplotlib.pyplot as plt
import matplotlib.dates
import scipy.stats as stats
import numpy
import datetime
import pandas
import calendar
import sys

from datetime import datetime
from collections import namedtuple


months = list(calendar.month_abbr[1:])
month_num = list(range(1,12))
def all_poems(csv_file):
	df = pandas.read_csv(csv_file, sep=';')
	df['date'] = pandas.to_datetime(df['date'], infer_datetime_format=True, errors = 'coerce')
	
	Results = namedtuple('Results', ['dates_ru', 'dates_ua', 'values_ua', 'values_ru'])

	dates_ru = []
	dates_ua = []
	values_ua = []
	values_ru = []
	for (id, row)  in df.iterrows():
		if (pandas.isnull(row.loc['date']) != True):
			if (row.loc['method'] == 'rubert_tiny2'):
				dates_ru.append(row.loc['date'])
				values_ru.append(row.loc['score'])
			if (row.loc['method'] == 'tonal_model_UA'):
				dates_ua.append(row.loc['date'])
				values_ua.append(row.loc['score'])

	return Results(dates_ru, dates_ua, values_ua, values_ru)
	
def sort_yearly_poems(csv_file):
	df = pandas.read_csv(csv_file, sep=';')
	df['date'] = pandas.to_datetime(df['date'], infer_datetime_format=True, errors = 'coerce')
	df.sort_values(by='date', inplace=True)
	df['year'] = pandas.DatetimeIndex(df['date']).year
	df['month'] = pandas.DatetimeIndex(df['date']).month

	Results = namedtuple('Results', ['year_min', 'year_max', 'poems_by_year'])

	yearMax = df['year'].max().astype(int)
	yearMin = df['year'].min().astype(int)

	poems_by_year = {}

	for i in range(0, (yearMax-yearMin)+1):
		poems = df.loc[df.date.dt.year.eq(yearMin+i)].values.tolist()
		poems_by_year[yearMin + i] = poems
		#print (str(yearMin+i) + ": " + str(len(poems)))

	return Results(yearMin, yearMax, poems_by_year)

def score_yearly_poems(poems_by_year, yearMin, yearMax):
	sentiment_ua_by_year = {}
	sentiment_ru_by_year = {}
	ru_count = []
	ua_count = []
	
	Results = namedtuple('Results', ['ua_score', 'ua_count', 'ru_score', 'ru_count'])

	for i in range(0, (yearMax-yearMin)+1):
		ru_count.append(0)
		ua_count.append(0)
		year = i+yearMin
		ua_score = 0.0
		ru_score = 0.0
		for j in range(0, len(poems_by_year[year])):
			if(poems_by_year[year][j][3] == 'tonal_model_UA'):
				ua_score = ua_score + poems_by_year[year][j][2]
				ua_count[i] = ua_count[i] + 1
			elif(poems_by_year[year][j][3] == 'rubert_tiny2'):
				ru_score = ru_score + poems_by_year[year][j][2]
				ru_count[i] = ru_count[i] + 1

		ua_score = ua_score/ua_count[i]
		ru_score = ru_score/ru_count[i]
		sentiment_ua_by_year[year] = (ua_score)
		sentiment_ru_by_year[year] = (ru_score)

	return Results(sentiment_ua_by_year, ua_count, sentiment_ru_by_year, ru_count)


def monthly_scored(year, poems_by_year):
	ru_score = [0.0]*12
	ru_count = [0]*12
	ua_score = [0.0]*12
	ua_count = [0]*12

	Results = namedtuple('Results', ['ua_score', 'ua_count', 'ru_score', 'ru_count'])


	for i in range(0, len(poems_by_year[year])):
		month = int(poems_by_year[year][i][6])-1
		if(poems_by_year[year][i][3] == 'tonal_model_UA'):
			ua_score[month] = ua_score[month] + poems_by_year[year][i][2]
			ua_count[month] = ua_count[month] +  1
		if(poems_by_year[year][i][3] == 'rubert_tiny2'):
			ru_score[month] = ru_score[month] + poems_by_year[year][i][2]
			ru_count[month] = ru_count[month] +  1

	for i in range(0,len(months)):
		if (ru_count[i] != 0):
			ru_score[i] = ru_score[i]/ru_count[i]
		else:
			ru_score[i] = 0

		if (ua_count[i] != 0):
			ua_score[i] = ua_score[i]/ua_count[i]
		else:
			ua_score[i] = 0

	return Results(ua_score, ua_count, ru_score, ru_count)

		#print(months[i] + " " + str(year) + ": \n")
		#print("\tUkrainian: " + str(ua_score[i]) + " | Total Poems: " + str(ua_count[i]))
		#print("\tRussian: " + str(ru_score[i]) + " | Total Poems: " + str(ru_count[i]))
		#print('\n')

def average_score_all_poems(poems_by_year, yearMin):
	ru_score = 0.0
	ua_score = 0.0
	ua_count = 0
	ru_count = 0
	Results = namedtuple('Results', ['ua_score', 'ru_score', 'ru_total', 'ua_total'])

	for i in range (0, len(poems_by_year)):
		year = i+yearMin
		for j in range(0, len(poems_by_year[year])):
			if(poems_by_year[year][i][3] == 'tonal_model_UA'):
				ua_score = ua_score + poems_by_year[year][j][2]
				ua_count = ua_count +  1
			if(poems_by_year[year][i][3] == 'rubert_tiny2'):
				ru_score = ru_score + poems_by_year[year][j][2]
				ru_count = ru_count +  1
	
	ua_score = ua_score/ua_count
	ru_score = ru_score/ru_count
	return Results(ua_score, ru_score, ru_count, ua_count)


def day_timestamp(poems_all):
	Results = namedtuple('Results', ['ru_times', 'ua_times', 'min_ru', 'min_ua'])
	times_ua = []
	times_ru = []
	for date in poems_all.dates_ua:
		times_ua.append(int(date.timestamp()))
		
	for date in poems_all.dates_ru:
		times_ru.append(int(date.timestamp()))

	min_ru = min(times_ru)
	min_ua = min(times_ua)
	print(min_ru)
	print(min_ua)
	for i in range (0,len(times_ua)):
		times_ua[i] = (times_ua[i] - min_ua)/(60*60*24)

	for i in range (0,len(times_ru)):
		times_ru[i] = (times_ru[i] - min_ru)/(60*60*24)

	
	print(times_ua)
	return Results(times_ru, times_ua, min_ru, min_ua)

def day_timestamp_by_year(poems_by_year, year):
	scores_ru = []
	times_ru = []
	scores_ua = []
	times_ua = []
	Results = namedtuple('Results', ['ru_times', 'ua_times', 'scores_ua', 'scores_ru'])

	for i in range(0, len(poems_by_year[year])):
		if(poems_by_year[year][i][3] == 'tonal_model_UA'):
			scores_ua.append(poems_by_year[year][i][2])
			times_ua.append(poems_by_year[year][i][4].timestamp())
		elif(poems_by_year[year][i][3] == 'rubert_tiny2'):
			scores_ru.append(poems_by_year[year][i][2])
			times_ru.append(poems_by_year[year][i][4].timestamp())
		
	min_ru = min(times_ru)
	min_ua = min(times_ua)
	print(min_ru)
	print(min_ua)
	for i in range (0,len(times_ua)):
		times_ua[i] = (times_ua[i] - min_ua)/(60*60*24)

	for i in range (0,len(times_ru)):
		times_ru[i] = (times_ru[i] - min_ru)/(60*60*24)

	return Results(times_ru, times_ua, scores_ua, scores_ru)

#print(delta_ru_2014)

year_sorted = sort_yearly_poems('sentiment_analysis.csv').poems_by_year
#year_scored = score_yearly_poems(year_sorted, 2013, 2023)
fig, axs = plt.subplots(1,2)

#MONTHLY PLOT
timestamp_2014 = day_timestamp_by_year(year_sorted, 2014)
axs[0].scatter(timestamp_2014.ua_times, timestamp_2014.scores_ua, c='b', label="Ukrainian")
axs[1].scatter(timestamp_2014.ru_times, timestamp_2014.scores_ru, c='r', label="Russian")
m0, b0 = numpy.polyfit(timestamp_2014.ua_times, timestamp_2014.scores_ua, 1)
y_line0 = m0*numpy.array(timestamp_2014.ua_times)+b0

m1, b1 = numpy.polyfit(timestamp_2014.ru_times, timestamp_2014.scores_ru, 1)
y_line1 = m1*numpy.array(timestamp_2014.ru_times)+b1
axs[0].plot(timestamp_2014.ua_times, y_line0, c="black")
axs[1].plot(timestamp_2014.ru_times, y_line1, c="black")

timestamp_2022 = day_timestamp_by_year(year_sorted, 2022)
#axs[0].scatter(timestamp_2022.ua_times, timestamp_2022.scores_ua, c='b', label="Ukrainian")
#axs[1].scatter(timestamp_2022.ru_times, timestamp_2022.scores_ru, c='r', label="Russian")
m2, b2 = numpy.polyfit(timestamp_2022.ua_times, timestamp_2022.scores_ua, 1)
y_line2 = m2*numpy.array(timestamp_2022.ua_times)+b2

m3, b3 = numpy.polyfit(timestamp_2022.ru_times, timestamp_2022.scores_ru, 1)
y_line3 = m3*numpy.array(timestamp_2022.ru_times)+b3
#axs[0].plot(timestamp_2022.ua_times, y_line2, c="black")
#axs[1].plot(timestamp_2022.ru_times, y_line3, c="black")

#print("UA_2014: y= " + str(round(m0,8)) + "x+" + str(round(b0,4)))
#print("RU_2014: y= " + str(round(m1,8)) + "x+" + str(round(b1,4)))

print("UA_2022: y= " + str(round(m2,8)) + "x+" + str(round(b2,4)))
print("RU_2022: y= " + str(round(m3,8)) + "x+" + str(round(b3,4)))
#TELEGRAM POEMS

#musakovska = all_poems('musakovska_analysis.csv')
#kazakov = all_poems('kazakov_analysis.csv')

#timestamp_m = day_timestamp(musakovska).ua_times
#timestamp_k = day_timestamp(kazakov).ru_times

#m0, b0 = numpy.polyfit(timestamp_m, musakovska.values_ua, 1)
#y_line0 = m0*numpy.array(timestamp_m)+b0

#m1, b1 = numpy.polyfit(timestamp_k, kazakov.values_ru, 1)
#y_line1 = m1*numpy.array(timestamp_k)+b1

#axs[0].scatter(timestamp_m, musakovska.values_ua, c='b')
#axs[1].scatter(timestamp_k, kazakov.values_ru, c='r')
#axs[0].plot(timestamp_m, y_line0, c="black")
#axs[1].plot(timestamp_k, y_line1, c="black")

#print("Musakovska: y= " + str(round(m0,8)) + "x+" + str(round(b0,4)))
#print("Kazakov: y= " + str(round(m1,8)) + "x+" + str(round(b1,4)))

#axs[0].scatter(musakovska.dates_ua, musakovska.values_ua, c='b')
#axs[0].set_title('Musakovska')

#axs[1].scatter(kazakov.dates_ru, kazakov.values_ru, c='r')
#axs[1].set_title('Kazakov')


#AVERAGES FOR ALL YEAR

#print(average_score_all_poems(year_sorted, 2013))

#years = []
#for i in range(0, 2024-2013):
#	years.append(i+2013)

#print(years)

#ALL POEMS SCATTER
#scatter_all = all_poems('sentiment_analysis.csv')
#timestamp_all = day_timestamp(scatter_all)

#m0, b0 = numpy.polyfit(timestamp_all.ua_times, scatter_all.values_ua, 1)
#m1, b1 = numpy.polyfit(timestamp_all.ru_times, scatter_all.values_ru, 1)
#yline_ua = m0*numpy.array(timestamp_all.ua_times) + b0
#yline_ru = m1*numpy.array(timestamp_all.ru_times) + b1

#axs[0].scatter(timestamp_all.ua_times, scatter_all.values_ua, c='b')
#axs[1].scatter(timestamp_all.ru_times, scatter_all.values_ru, c='r')
#axs[0].plot(timestamp_all.ua_times, yline_ua, c="black")
#axs[1].plot(timestamp_all.ru_times, yline_ru, c="black")

#print("Ukrainian: y= " + str(round(m0,8)) + "x+" + str(round(b0,4)))
#print("Russian: y= " + str(round(m1,8)) + "x+" + str(round(b1,4)))







#delta_ua_2022 = [0]
#delta_ru_2022 = [0]
#delta_ua_2014 = [0]
#delta_ru_2014 = [0]

#for i in range(1, 12):
	
#	delta_ua_2022.append(month_2022.ua_score[i] - month_2022.ua_score[i-1])
#	delta_ru_2022.append(month_2022.ru_score[i] - month_2022.ru_score[i-1])

#	delta_ua_2014.append(month_2014.ua_score[i] - month_2014.ua_score[i-1])
#	delta_ru_2014.append(month_2014.ru_score[i] - month_2014.ru_score[i-1])


#MONTHLY AVERAGES

month_2014 = monthly_scored(2014, year_sorted)
month_2022 = monthly_scored(2022, year_sorted)

#axs[0].scatter(months, month_2014.ua_score, c='b', label="Ukrainian")
#axs[0].scatter(months, month_2014.ru_score, c='r', label="Russian")
#axs[0].set_title('Sentiment score for 2014')

#axs[0,1].plot(months, delta_ua_2014, c='b', label="Ukrainian")
#axs[0,1].plot(months, delta_ru_2014, c='r', label="Russian")
#axs[0,1].set_title('Change in sentiment 2014')

#axs[0].plot(months, month_2014.ua_count, c='b', label="Ukrainian")
#axs[0].plot(months, month_2014.ru_count, c='r', label="Russian")
#axs[0].set_title('Poems per month 2014')

#axs[1].scatter(months, month_2022.ua_score, c='b', label="Ukrainian")
#axs[1].scatter(months, month_2022.ru_score, c='r', label="Russian")
#axs[1].set_title('Sentiment score for 2022')

#axs[1,1].plot(months, delta_ua_2022, c='b', label="Ukrainian")
#axs[1,1].plot(months, delta_ru_2022, c='r', label="Russian")
#axs[1,1].set_title('Change in sentiment 2022')

#axs[1].plot(months, month_2022.ua_count, c='b', label="Ukrainian")
#axs[1].plot(months, month_2022.ru_count, c='r', label="Russian")
#axs[1].set_title('Poems per month 2022')



#axs[0,0].scatter(months, month_2014.ua_score)
#axs[0,0].set_title('Sentiment score by month in 2014 (Ukr)')
#axs[1,0].bar(months, month_2014.ua_count)
#axs[1,0].set_title('Number of poems archived by month in 2014 (Ukr)')

#axs[0,1].scatter(months, month_2022.ua_score)
#axs[0,1].set_title('Sentiment score by month in 2022 (Ukr)')
#axs[1,1].bar(months, month_2022.ua_count)
#axs[1,1].set_title('Number of poems archived by month in 2022 (Ukr)')

#axs[0,1].scatter(months, month_2014.ru_score)
#axs[0,1].set_title('Sentiment score by month in 2014 (Rus)')
#axs[1,1].bar(months, month_2014.ru_count)
#axs[1,1].set_title('Number of poems archived by month in 2014 (Rus)')

#axs[0,2].scatter(months, (numpy.array(month_2014.ru_score) + numpy.array(month_2014.ua_score)))
#axs[0,2].set_title('Sentiment score by month in 2014 (Combined)')
#axs[1,2].bar(months, (numpy.array(month_2014.ru_count) + numpy.array(month_2014.ua_count)))
#axs[1,2].set_title('Number of poems archived by month in 2014 (Combined)')

#axs[0,1].scatter(months, month_2022.ru_score)
#axs[0,1].set_title('Sentiment score by month in 2022 (Rus)')
#axs[1,1].bar(months, month_2022.ru_count)
#axs[1,1].set_title('Number of poems archived by month in 2022 (Rus)')


#[[90, 1.0, -15.287094864994287, 'tonal_model_UA', Timestamp('2013-12-06 00:00:00'), 2013.0, 12.0], [263, 2.0, -2.2381147742271423, 'tonal_model_UA', Timestamp('2013-12-26 00:00:00'), 2013.0, 12.0], [91, 3.0, -0.3007555902004242, 'dostoevsky', Timestamp('2013-12-27 00:00:00'), 2013.0, 12.0], [264, 4.0, 0.3007555902004242, 'dostoevsky', Timestamp('2013-12-31 00:00:00'), 2013.0, 12.0]]

#axs[0].scatter(years, year_scored.ru_score.values(), c='r', label='Russian')
#axs[0].set_title('Sentiment')
#axs[1].bar(years, year_scored.ru_count, color='r', label='Russian')
#axs[0,1].scatter(years, year_scored.ru_count)
#axs[1].set_title('Number of Poems')
plt.show()