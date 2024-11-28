from flask import Flask, render_template, request, redirect, url_for, send_file
import requests
import os

app = Flask(__name__)
YANDEX_API_BASE_URL = "https://cloud-api.yandex.net/v1/"
