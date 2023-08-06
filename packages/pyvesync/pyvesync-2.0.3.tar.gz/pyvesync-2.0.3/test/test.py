import pyvesync.vesync as vs

a = vs.VeSync('jtrabulsy@gmail.com', 'M!cr0$0ft', debug=True)
a.login()
a.update()
b = a.fans[0]
b.update()

a.outlets()