library(lubridate)

############ time_series_covid19_confirmed_US ############
tsurl = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv"
df = read.csv(tsurl, check.names=FALSE,stringsAsFactors=FALSE)
names(df)<-tolower(names(df))
df$province_state <- tolower(df$province_state)
df$admin2 <- tolower(df$admin2)
df<-df[!df$lat%in%0,]
sdm<-df[csdm<-df[c(6,7,(length(df)-90):length(df))]
names(sdm)<-tolower(names(sdm))
tsdates = names(sdm[c(3:length(sdm))])

