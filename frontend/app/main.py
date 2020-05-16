# -*- coding: utf-8 -*-
import requests
import json
import datetime

import streamlit as st
import pandas as pd
import altair as alt


st.title("Words Record")
st.write("Words tracking and analysis")

def preprocess_data(raw_data):
    data = raw_data.sort_values(by="create_time", ascending=True).reset_index(drop=True)
    data = data[["id", "words_num", "create_time"]]
    data["timestamp"] = pd.to_datetime(data["create_time"])
    data["date"] = data["timestamp"].dt.date
    data["year_month"] = data["timestamp"].dt.strftime("%Y-%m")
    data["year_week"] = data["timestamp"].dt.strftime("%Y-%W")
    data["month_of_year"] = data["timestamp"].dt.month
    data["week_of_year"] = data["timestamp"].dt.week
    data["day_of_week"] = data["timestamp"].dt.dayofweek
    data["day_name"] = data["timestamp"].dt.day_name()
    data["diff"] = data.groupby("year_month")["words_num"].diff().fillna(0)
    return data

@st.cache
def load_data():
    response = requests.get("http://192.168.148.129:8002/api/v1.0/word")
    raw_data = pd.DataFrame(response.json())
    data = preprocess_data(raw_data)
    return data


data = load_data()

st.sidebar.title("Options")
st.sidebar.subheader("Show raw data")
show_raw_data = st.sidebar.checkbox("Show raw data")

if show_raw_data:
    st.dataframe(data[["id", "words_num", "create_time"]])

d = pd.to_datetime(st.date_input("words loss since:", data.timestamp.min()))

c1 = (
    alt.Chart(data[data.timestamp > d])
    .mark_line(color="#1E90FF", size=1)
    .encode(
        alt.Y(
            "words_num",
            scale=alt.Scale(domain=[data.words_num.max() * 0.8, data.words_num.max()]),
            title="words record",
        ),
        x="date:T",
        tooltip=["id", "words_num"],
    )
    .properties(height=400, width=300)
    .interactive()
)

c2 = (
    alt.Chart(data[data.timestamp > d].groupby("year_week")["diff"].sum().reset_index())
    .mark_bar()
    .encode(
        y=alt.Y("year_week", title="week"),
        x=alt.X("diff:Q", title="difference to day before"),
        color=alt.condition(
            alt.datum.diff < 0,
            alt.value("#ADFF2F"),  # The positive color
            alt.value("#D2691E"),  # The negative color
        ),
        tooltip=["diff"],
    )
    .properties(height=400, width=200)
    .interactive()
)

c3 = c1 | c2

st.altair_chart(c3, use_container_width=True)

weekdays = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

options = st.selectbox(
    "words_num loss by week:",
    data.year_week.unique().tolist(),
    index=data.year_week.unique().tolist().index(data.year_week.unique().tolist()[-1]),
)

c4 = (
    alt.Chart(data[data.year_week == options])
    .mark_circle(color="black")
    .encode(
        y=alt.Y(
            "words_num",
            scale=alt.Scale(
                domain=[
                    data[data.year_week == options].words_num.max() * 0.95,
                    data[data.year_week == options].words_num.max(),
                ]
            ),
            title="words_num",
        ),
        x=alt.X("day_name", sort=weekdays, title="day of week"),
        tooltip=["words_num", "create_time"],
    )
    .interactive()
)

st.altair_chart(c4, use_container_width=True)

c5 = (
    alt.Chart(data)
    .mark_circle(color="black")
    .encode(
        x=alt.X("diff", title="difference to day before"),
        y=alt.Y("day_name", sort=weekdays, title="day of week"),
        color=alt.condition(
            alt.datum.diff < 0,
            alt.value("#50fa7b"),  # The positive color
            alt.value("#ff5555"),  # The negative color
        ),
    )
    .configure_mark(opacity=0.3)
)


st.altair_chart(c5, use_container_width=True)

st.sidebar.subheader("Add words_num")
words_num = st.sidebar.number_input("words_num")
date = st.sidebar.date_input("Measured at:")
date = datetime.datetime(date.year, date.month, date.day)


if st.sidebar.button("add"):
    response = requests.post(
        "http://192.168.148.129:8002/api/v1.0/word",
        data=json.dumps({"words_num": words_num, "create_time": str(date)}),
    )
    if response.status_code == 201:
        st.sidebar.success("words_num added")
    else:
        st.sidebar.exception(RuntimeError("words_num could not be added"))


st.sidebar.subheader("Delete words_num")
del_id = int(st.sidebar.number_input("id"))

if st.sidebar.button("delete"):
    response = requests.delete(f"http://192.168.148.129:8002/api/v1.0/word/{del_id}")
    if response.status_code == 200:
        st.sidebar.success("words_num deleted")
    else:
        st.sidebar.exception(
            RuntimeError(f"No words_num found at id:{del_id} could not be deleted")
        )
