from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
import time
import math
import sys
from datetime import datetime

from autoblog import post_blog
from configmanager import config

def task():
    print("Task: Posting blog")
    post_blog(config['shopify_store'], config['shopify_access_token'], config['neetsai_api_key'], config['shopify_blog_id'])

class Job:
    def __init__(self, jobClass, freq):
        self.jobClass = jobClass
        self.frequency = freq

class Scheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.jobs = {}
        self.running = False

    def getCronTrigger(self, times_per_wk):
        # Calculate the intervals in hours and distribute them over a week
        days_of_week = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
        times_per_wk = max(int(times_per_wk),1)

        days_of_week_str = []
        hours_str = []
        hours = []

        if times_per_wk <= 7:
            i = 0
            step = 7 / times_per_wk
            while i < 7:
                days_of_week_str.append(days_of_week[math.floor(i)])
                i = i + step
            hours.append(0)
        else:
            days_of_week_str = days_of_week
            times_per_day = times_per_wk // 7
            for i in range(min(times_per_day,24)):
                hours.append(i)

        days_of_week_str = ','.join(map(str, set(days_of_week)))
        hours_str = ','.join(map(str, hours))

        trigger = CronTrigger(
            year='*', month='*', day='*', week='*', day_of_week=days_of_week_str, hour=hours_str, minute=0, second=0
        )

        return trigger

    def start(self, times_per_wk):
        if not self.running:
            self.scheduler.start()

            job = self.scheduler.add_job(task, trigger=self.getCronTrigger(times_per_wk), name="AutoBlog")
            self.jobs["AutoBlog"] = Job(job, times_per_wk)

            self.running = True
            print('start')

    def stop(self):
        if self.running:
            self.scheduler.shutdown()
            self.running = False
            print('stop')

    def add_job(self, job_name, interval_seconds=60):
        if job_name not in self.jobs:
            pass

    def remove_job(self, job_id):
        #TODO job name
        if job_id in self.jobs:
            self.scheduler.remove_job(job_id)
            del self.jobs[job_id]
            print(f"Job {job_id} removed.")

    def edit_interval(self, job_name, times_per_wk):
        if job_name in self.jobs:
            job = self.jobs[job_name]
            job.jobClass.reschedule(trigger=self.getCronTrigger(times_per_wk))
            job.frequency = times_per_wk
            print(f"Job {job_name} rescheduled with new times_per_wk={times_per_wk}.")

    def get_status(self):
        status = {
            "running": self.running,
            "jobs": []
        }
        for job_name, job in self.jobs.items():
            next_run = job.jobClass.next_run_time.isoformat() if job.jobClass.next_run_time else None
            job_status = {
                "job_name": job_name,
                "next_run": next_run,
                "interval": job.frequency
            }
            status["jobs"].append(job_status)
        return status
