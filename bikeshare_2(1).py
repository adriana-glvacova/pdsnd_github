import time
import pandas as pd
import numpy as np


CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = input("Enter a city (Chicago / New York City / Washington): ").lower()
    while city not in CITY_DATA.keys():
        print("Invalid input.\n")
        city = input("Enter a city (Chicago / New York City / Washington): ").lower()

    # get user input for month (all, january, february, ... , june)
    valid_months = ['january', 'february', 'march', 'april', 'may', 'june']
    month = input("Enter a month (jan-jun): ").lower()

    while month not in valid_months and month != 'all':
        print("Invalid input.\n")
        month = input("Enter a month (jan-jun): ").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    valid_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = input("Enter a day of the week (mon-sun): ").lower()

    while day not in valid_days and day != 'all':
        print("Invalid input.\n")
        day = input("Enter a day of the week (mon-sun): ").lower()

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

    df = pd.read_csv(CITY_DATA[city], parse_dates=['Start Time', 'End Time'])
    df['Start month string'] = pd.DatetimeIndex(df['Start Time']).month_name()
    df['Start day string'] = pd.DatetimeIndex(df['Start Time']).day_name()

    if month != 'all':
        month_filter = df['Start month string'] == month.capitalize()
        df = df[month_filter]

    if day != 'all':
        day_filter = df['Start day string'] == day.capitalize()
        df = df[day_filter]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['Start month string'].mode()[0]
    print('Most common month:\t', most_common_month)

    # display the most common day of week
    most_common_day = df['Start day string'].mode()[0]
    print('Most common day of week:\t', most_common_day)

    # display the most common start hour
    df['Start Hour'] = df['Start Time'].dt.hour
    most_common_start_hour = df['Start Hour'].mode()[0]
    print('Most common start hour:', most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def start_station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('Most common start station:\t', most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('Most common end station:\t', most_common_end_station)

    # display most frequent combination of start station and end station trip
    temp = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False)
    temp = temp.index[0]
    print('Most frequent trip:\t\t\t', temp[0], '-', temp[1])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time = time.strftime("%H:%M:%S", time.gmtime(total_travel_time))
    print('Total travel time:\t', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time:\t', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df['User Type'].value_counts().to_frame(name=''))

    # Display counts of gender
    if 'Gender' in df.columns:
        num_of_males = (df.Gender == 'Male').sum()
        num_of_females = (df.Gender == 'Female').sum()

        print('\n')
        print('No. of males:\t', num_of_males)
        print('No. of females:\t', num_of_females)
    else:
        print('No gender information available.')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = min(df['Birth Year'])
        most_recent_year = max(df['Birth Year'])
        most_frequent_year = df['Birth Year'].mode()[0]

        print('\n')
        print('Earliest year of birth:\t', earliest_year)
        print('Most recent year of birth:\t', most_recent_year)
        print('Most frequent year of birth:\t', most_frequent_year)
    else:
        print('No birth year information available.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def print_raw_data(df):

    user_input = input('\n\nWould you like to see raw data? (yes/no): ').lower()
    index = 0

    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    df.rename(columns={'Unnamed: 0': 'No.'}, inplace=True)

    while True:
        if user_input == 'yes':
            print('\n')
            print(df.iloc[index:(index+5)])
            index = index + 5
        elif user_input == 'no':
            break
        else:
            print('Invalid input.\n')

        user_input = input('\nContinue? (yes/no): ').lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        start_station_stats(df)
        trip_stats(df)
        user_stats(df)

        print_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
