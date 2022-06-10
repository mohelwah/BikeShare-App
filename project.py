# -*- coding: utf-8 -*-
"""
Created on Sun Jan  9 22:22:37 2022

@author: root
"""

import time
import pandas as pd
import numpy as np

city_dict = {'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}

month_list = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

day_list = ['all', 'monday', 'tuesday', 'wednesday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    #  get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_name = ''
    while city_name.lower() not in city_dict:
        city_name = input("\nWhoud you like to analyse data for: \n 1- Chicago \n 2- New york city\n 3- Washington\n Enter Your choise: ")
        if city_name.lower() in city_dict:
            city = city_dict[city_name.lower()]
        else:
            print("Error, please select a correct option from above\n")

    #  get user input for month (all, january, february, ... , june)
    month_name = ''
    while month_name.lower() not in month_list:
        print('\nWhat is the name of the month to filter data?')
        for month in month_list:
            print('- ', month)
        month_name = input("Enter your choice: ")
        if month_name.lower() in month_list:
            #set the month value
            month = month_name.lower()
        else:
             # print error
            print("Error, please select a correct option from above\n")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_name = ''
    while day_name.lower() not in day_list:
        print('\nWhat is the name of the day to filter data?')
        for day in day_list:
            print('- ', day)
        day_name = input("Enter your choice: ")
        if day_name.lower() in day_list:
            day = day_name.lower()
        else:
            #Error
            print("Error, please select a correct option from above\n")

    print('-'*40)
    return city, month, day



def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(city)
    #convert start time from object to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour

    # made a filter using month
    if month != 'all':
        month = month_list.index(month)
        df = df.loc[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        df = df.loc[df['day_of_week'] == day.title()]

    return df



def time_stats(df,month_list=month_list):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    df['month'] =df['Start Time'].dt.month
    popular_month_index = int(df['month'].mode()[0])
    print('Most Frequent common month:', month_list[popular_month_index])


    #   display the most common day of week
    df['day'] =df['Start Time'].dt.weekday
    popular_day = df['day'].mode()[0]
    print('Most Frequent day of week:', popular_day)


    #   display the most common start hour
    df['hour'] =df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Frequent Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()


    start_station = df['Start Station'].mode()[0]
    print('most commonly used start station: {}'.format(start_station))

    #   display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('most commonly used end station: {}'.format(end_station))

    #   display most frequent combination of start station and end station trip
#    freq_combination = (df['Start Station'] + "," + df['End Station']).mode()[0]
#    print("The most frequent combination of start station and end station trip is : " + str(freq_combination.split(",")))
    # Another good code for commbination of start and end station
    most_popular_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print("The most frequent combination of start station and end station trip is : " + str(most_popular_trip))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #   display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('total travel time: {}'.format(total_travel_time))

    #   display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('mean travel time: {}'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #   Display counts of user types User Type
    print('The count of user types',df['User Type'].value_counts())



    #   Display earliest, most recent, and most common year of birth
    if city == 'chicago.csv' or city == 'new_york_city.csv':
    #   Display counts of gender
        print(df['Gender'].value_counts())
        earliest = df['Birth Year'].min()
        recent = df['Birth Year'].max()
        most_common = df['Birth Year'].mode()[0]

        print('Earlist year of birth is: {}'.format(earliest))
        print('most recent year of birth is: {}'.format(recent))
        print('most common year of birth is: {}'.format(most_common))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

def display_raw_data(df):
    """Displays data head request.

    Input:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    Return:
         Print DataFrame Head
    """
    print(df.head())
    next = 0
    while True:
        view_raw_data = input('\nwould you like to view next five row of raw data? Enter: yes | no.\n')
        if view_raw_data.lower() != 'yes':
            return
        next = next + 5
        print(df.iloc[next:next+5])


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        while True:
            view_raw_data = input('\nwould you like to view first 5 row of data? Enter: yes | no.\n')
            if view_raw_data.lower() != 'yes':
                break
            display_raw_data(df)
            break

        restart = input('\nWould you like to restart? Enter: yes | no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
