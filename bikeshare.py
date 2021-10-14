# DO NOT delete below this line ==============
import time
import pandas as pd
import numpy as np
# DO NOT delete above this line ==============

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities = ['chicago','new york city','washington']
months = ['all','january','february','march','april','may','june']
days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']

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
    while True:
        try:
            city = str(input('\nEnter a city of interest. Data currently available for Chicago, New York City, and Washington :')).lower()
        except ValueError:
            print('\nString is expected, let\'s try again shall we?')
            continue
        else:
            if city in cities:
                break
            else: 
                print('\nThere is no data for the provided city, check spelling and try again')
                continue


    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = str(input('\nEnter a month between January and June to filter data, or enter ALL for no filter :')).lower()
        except ValueError:
            print('String is expected, let\'s try again shall we?')
            continue
        else:
            if month in months:
                break
            else: 
                print('\nThere is no data for the provided month, check spelling and try again')
                continue


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = str(input('\nEnter a day of the week to filter data, or enter ALL for no filter :')).lower()
        except ValueError:
            print('String is expected, let\'s try again shall we?')
            continue
        else:
            if day in days:
                break
            else: 
                print('\nThere is no data for the provided day, check spelling and try again')
                continue

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
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month)
    
        # filter by month to create the new dataframe
        df = df[(df['month'] == month)]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
       
        df = df[(df['day_of_week'] == day.title())]
    
    return df

def find_common(df, column_name):
    """
    This will take column name and return the most frequent item name and number of occurence.

    Args:
        (dataframe) df - the dataframe to work on
        (str) column_name - name of the column to analyze on the dataframe
        
    Returns:
        item_name - name of the item with the highest occurence in the column
        occurence - number of occurence of the item in the column
    """
    #First we get the common item, then the occurence
    item_name = df[column_name].mode()[0]
    
    occurence = df.loc[df[column_name] == item_name].count()[0]
    
    return item_name, occurence
    

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    #First we get the common month and the occurence
    common_month, month_occurence = find_common(df,'month')
    
    print('\nThe most common MONTH is {} with {:,} occurences'.format(months[common_month].title(), month_occurence))

    # display the most common day of week
    #First we get the common day-of-week (dow) and the occurence
    common_dow, dow_occurence = find_common(df,'day_of_week')
    
    print('\nThe most common DAY OF WEEK is {} with {:,} occurences'.format(common_dow, dow_occurence))

    # display the most common start hour
    #First we get the common start-hour (sth) and the occurence
    common_sth, sth_occurence = find_common(df,'hour')

    print('\nThe most common START HOUR is {} with {:,} occurences'.format(common_sth, sth_occurence))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station (sts)
    common_sts, sts_occurence = find_common(df,'Start Station')

    print('\nThe most common START STATION is {} with {:,} occurences'.format(common_sts, sts_occurence))

    # display most commonly used end station (ens)
    common_ens, ens_occurence = find_common(df,'End Station')

    print('\nThe most common END STATION is {} with {:,} occurences'.format(common_ens, ens_occurence))

    # display most frequent combination of start station and end station trip (combine_station)
    """ The code below works well on my desktop but not working on your workspace so i had to rewrite

    combine_station = df.value_counts(['Start Station','End Station']).head(1)
    combine_station_name = combine_station.index.tolist()[0]
    combine_station_occurence = combine_station[0]
    
    print('The most common COMBINED STATION is FROM {} TO {} with {:,} occurences'.format((*combine_station_name), combine_station_occurence))

    it ends here """
    
    combine_station = pd.Series(df['Start Station'] +' TO ' + df['End Station']).mode()[0]
    combine_station_occurence = pd.Series(df['Start Station'] +' TO ' + df['End Station']).value_counts()[0] #this method result in DESC order

    print('\nThe most common COMBINED STATION is FROM {} with {:,} occurences'.format(combine_station, combine_station_occurence))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_traveltime = (df['Trip Duration'].sum()) / 3600 #hour conversion
    print('\nTotal travel time is approximately {:,.0f} Hours'.format(total_traveltime))


    # display mean travel time
    mean_traveltime = (df['Trip Duration'].mean()) / 60 #minutes conversion
    print('\nMean travel time is approximately {:,.0f} Minutes'.format(mean_traveltime))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    
    #we will validate each column before performing action as some of the data files have missing columns

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #  Display counts of user types
    if 'User Type' in df.columns:
        user_types = df.groupby(['User Type']).size().to_frame('Count').reset_index() # i researched how to use to_frame() via GitHub
        print('\nCount of User Types within the DataFrame: \n')
    
        print(user_types)
    else:
        print('\nNo \'User Type\' Column in data')

    #  Display counts of gender
    if 'Gender' in df.columns :
        gender = df.groupby(['Gender']).size().to_frame('Count').reset_index()
        print('\nCount of Gender within the DataFrame: \n')
    
        print(gender)
    else:
        print('\nNo \'Gender\' Column in data')

    #  Display earliest, most recent, and most common year of birth => (yob)
    if 'Birth Year' in df.columns:
        earliest_yob = int(df['Birth Year'].min())
        recent_yob = int(df['Birth Year'].max())
        common_yob = int(df['Birth Year'].mode()[0])
    
        print('\nYear of Birth statistics:\nEARLIEST - {:.0f} \nMOST RECENT - {:.0f} \nMOST COMMON -{:.0f} '.format(earliest_yob, recent_yob, common_yob))
    else:
        print('\nNo \'Birth Year\' Column in data')
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_data(df):
    """ this will be used to slice throught the dataframe and display 5 records per page """
    
    print('\nDisplaying DataFrame 5 rows per page\n')
    start, stop = 0, 5
        
    while True:
        print(df[start : (start+stop)])
        start += stop

        #check if request is still within dataframe content range
        if (start >= df.count()[0]):
            print('\nYou have reached the end of the data')
            break

        #get feedback from users on more data display    
        more_data = str(input('\nEnter NEXT to show more data or STOP to cancel:'))
        if (more_data.lower() != 'next'):
            break
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        print('DATA USED: {}, Filtered with MONTH: {} and DAY: {}'.format(city.title(), month.title(), day.title()))
        show_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('\nSee you some other time. Good bye!')
            break


if __name__ == "__main__":
	main()