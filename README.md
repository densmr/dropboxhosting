Proxy for Dropbox Hosting
==============

## Summary
A GAE proxy to your Dropbox account.

## Description
This project aims to allow you to use your own domain to get site published in your Dropbox. So, after setting up your Dropbox account number at the application and publish it on Google App Engine (GAE), you will access your site in the Dropbox linking them to a more significant domain than that presented by URL http://dl.dropbox.com/u/YOURDROPBOXNUMBER.

This code is a very simple reduction/adaptation of [DropbProx](http://code.google.com/p/dropbprox/) project (by [Paulo Jerônimo](http://paulojeronimo.com)) held specifically to add default page for site hostings.

## Installation
1. **Create a new project on GAE.**
For example, I created a project named pj74arqs. A good tutorial about how to do this (for windows users) is the post "[Setup your own Proxy Server in 5 Minutes for Free](http://www.labnol.org/internet/setup-proxy-server/12890/)"
2. **Change application variable** at file app.yaml to the name of your created project on GAE;
3. **Change DROPBOX_PREFIX variable** at file mirror.py to your own Dropbox address;
 - If you use Public folder, it should looks like dl.dropbox.com/u/123456 where 123456 — your Dropbox number
 - If you use [Static Web Apps application](Static Web Apps application), it should looks like dl.dropbox.com/spa/1q2w3e4r5t6y7u8 where 1q2w3e4r5t6y7u8 — your unique personal number
4. **Publish the application on GAE**;
 - Windows users: see [this](http://www.labnol.org/internet/setup-proxy-server/12890/) post;
5. *Optional*: Change the domain of the published application.
In my case, after publish the application, the domain was densmr.appspot.com. But, this wasn't good for me yet. So, I changed the URL for that application to my subdomain: www.densmr.com using Google Apps Control Panel.

## Use
Instead of access your files using the Dropbox URL (http://dl.dropbox.com/u/YOURDROPBOXNUMBER) you can now use the GAE application URL.
For example, the page http://dl.dropbox.com/spa/7k4i6qqjxq9yxvc/site/public/index.html and http://densmr.ru (my personal Russian site) is the same.
Update a file in your Dropbox account and refresh your URL. You will see that was updated in your proxy too!