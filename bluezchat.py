import os
import sys         # for sys.exit
import time        # to get current timestamp
import threading   # for threads
import socket      # wifi sockets
import datetime    # for datetime column in db

try:
    import sqlite3
    conn = sqlite3.connect("bluezchat.db") # create new database connection
except:
    print "Install sqlite3 first"

try:
    import gtk
    import gobject
    import gtk.glade  # gtk is interface, gobject is event handler for gtk
except:
    print "Please install gtk, gobject and glade packages for Python, exiting."
    print "sudo apt-get install python-gtk2 python-glade2 python-gobject"
    sys.exit()

try:
    import netifaces # this is required to get wifi IP and check if connected to wifi
except:
    print "Install netifaces"
    print "sudo easy_install netifaces"
    sys.exit()

bluetoothAvailability = None

# try to import bluetooth, if it is not found, disable bluetooth
try:
    import bluetooth
except:
    bluetoothAvailability = False
    print "I can\'t use bluetooth in your system, sorry mate :("

# try to open a temporary socket to test if bluetooth is on on the device
# if this raises an error, bluetooth is disabled on the device
if bluetoothAvailability != False:
    try:
        bluetoothAvailability = True
        tempSock = bluetooth.BluetoothSocket(bluetooth.L2CAP)
        tempSock.settimeout(1)
        tempSock.connect(("01:23:45:67:89:AB", 0x1001))
    except Exception as e:
        if "No route to host" in str(e):
            print "There's something wrong with bluetooth, disabling it"
            bluetoothAvailability = False

# try to get IP address of the device, if not wi-fi will be disabled
wifi_availability = None
try:
    print "IP: %s" % (netifaces.ifaddresses(netifaces.gateways()['default'][netifaces.AF_INET][1])[netifaces.AF_INET][0]['addr'])
    print "Wi-fi interface found"
    wifi_availability = True
except:
    print "Wi-fi is not connected, disabling..."
    wifi_availability = False

# print wfi and bluetooth status, if both are disabled exit
if wifi_availability and bluetoothAvailability:
    print "Wi-Fi and bluetooth are both nice and working."
elif wifi_availability:
    print "Wifi is working, bluetooth is not"
elif bluetoothAvailability:
    print "Bluetooth is nice and working, wi-fi is not."
else:
    print "You can't use this program without wifi or bluetooth, exiting..."
    sys.exit()

# *****************

GLADEFILE="bluezchat.glade"

def alert(text, buttons=gtk.BUTTONS_NONE, type=gtk.MESSAGE_INFO):
    md = gtk.MessageDialog(buttons=buttons, type=type)
    md.label.set_text(text)
    md.run()
    md.destroy()

class BluezChatGui:
    def __init__(self):
        self.main_window_xml = gtk.glade.XML(GLADEFILE, "bluezchat_window")

        # connect our signal handlers
        dic = { "on_quit_button_clicked" : self.quit_button_clicked,
                "on_send_button_clicked" : self.send_button_clicked,
                "on_scan_button_clicked" : self.scan_button_clicked,
                "on_devices_tv_cursor_changed" : self.devices_tv_cursor_changed
                }

        self.main_window_xml.signal_autoconnect(dic)

        # prepare the floor listbox
        self.devices_tv = self.main_window_xml.get_widget("devices_tv")
        self.discovered = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING)
        self.devices_tv.set_model(self.discovered)
        renderer = gtk.CellRendererText()
        column1=gtk.TreeViewColumn("addr", renderer, text=0)
        column2=gtk.TreeViewColumn("name", renderer, text=1)
        self.devices_tv.append_column(column1)
        self.devices_tv.append_column(column2)

        self.quit_button = self.main_window_xml.get_widget("quit_button")
        self.scan_button = self.main_window_xml.get_widget("scan_button")

        self.send_button = self.main_window_xml.get_widget("send_button")
        self.main_text = self.main_window_xml.get_widget("main_text")
        self.text_buffer = self.main_text.get_buffer()

        self.input_tb = self.main_window_xml.get_widget("input_tb")
        self.input_tb2 = self.main_window_xml.get_widget("input_tb2")

        self.listed_devs = []

        self.peers = {}
        self.sources = {}
        self.addresses = {}
        self.hosts = {}
        self.messages = []
        self.thread_list = []

        # the listening sockets
        self.server_sock = None
        self.server_sock_wifi = None
        self.hostname = socket.gethostname()
        self.server_IP = None
        self.server_IP_template = None
        self.wifi_port = None
        self.wifi = wifi_availability
        if wifi_availability:
            self.server_IP = netifaces.ifaddresses(netifaces.gateways()['default'][netifaces.AF_INET][1])[netifaces.AF_INET][0]['addr']
            self.server_IP_template = self.server_IP[:9]
            self.wifi_port = 12345
        self.bluetooth = bluetoothAvailability
        self.bluetoothConnType = bluetooth.L2CAP
        self.bluetoothPort = 0x1001
        self.timeout = 10

# --- gui signal handlers

    def quit_button_clicked(self, widget):
        gtk.main_quit()

    def scan_button_clicked(self, widget):
        self.quit_button.set_sensitive(False)
        self.scan_button.set_sensitive(False)
        self.discovered.clear()

        # Inititiate WIFI Scan ##############################################

        if self.wifi:
            ip_ = 1
            while ip_ < 255:
                ip_ = ip_ + 1
                IP = self.server_IP_template + str(ip_)
                if IP == self.server_IP:
                    continue
                # Create two threads as follows
                try:
                    t = threading.Thread(target=self.discover, args=(IP,))
                    # Sticks the thread in a list so that it remains accessible
                    self.thread_list.append(t)
                except Exception as e:
                    template = "An exception of type {0} occured. Arguments:{1!r}"
                    mesg = template.format(type(e).__name__, e.args)
                    print mesg

            for thread in self.thread_list:
                thread.start()

            for thread in self.thread_list:
                thread.join()

            del self.thread_list[:]
        else:
            "Wifi scan skipped, not connected to wifi."

        # Initiate bluetooth scan ###########################################
        
        if self.bluetooth:
            for addr, name in bluetooth.discover_devices (lookup_names = True):
                print "(%s, %s)" % (addr, name)
                try:
                    t = threading.Thread(target=self.discover_bluetooth, args=(addr, name,))
                    # Sticks the thread in a list so that it remains accessible
                    self.thread_list.append(t)
                except Exception as e:
                    template = "An exception of type {0} occured. Arguments:{1!r}"
                    mesg = template.format(type(e).__name__, e.args)
                    print mesg

            for thread in self.thread_list:
                thread.start()

            for thread in self.thread_list:
                thread.join()

            del self.thread_list[:]

        self.quit_button.set_sensitive(True)
        self.scan_button.set_sensitive(True)

        print "Done"

    def send_button_clicked(self, widget):
        text =  str(int(time.time()) % 1000) + "," + self.hostname + "," + self.input_tb2.get_text() + "," + self.input_tb.get_text()
        if len(text) == 0: return
        #we can store input_tb2.get_text() before the text = line, may be it can be changed
        if self.input_tb2.get_text() not in self.hosts:
            conn.execute("INSERT INTO messages VALUES (?, ?, ?, ?, ?)", (str(int(time.time()) % 1000), self.hostname, self.input_tb2.get_text(), datetime.datetime.now(), self.input_tb.get_text()))
            conn.commit()

        for addr, sock in list(self.peers.items()):
            try:
                sock.send(text)
                print "sent to ", sock
            except Exception as e:
                template = "An exception of type {0} occured. Arguments:{1!r}"
                mesg = template.format(type(e).__name__, e.args)
                print mesg
                continue

        self.input_tb.set_text("")
        s_data_arr = text.split(",")
        message = s_data_arr[3]
        #we can concanete the whole message here, before printing it. Because it can contain commas
        self.add_text("\n%s: %s" % (self.hostname, message))

    

    def devices_tv_cursor_changed(self, widget):
        (model, iter) = self.devices_tv.get_selection().get_selected()
        self.input_tb2.set_text(model.get_value(iter, 1))
       

# --- network events

    def get_data(self, mhash, host, dest, mtime, message):
        return str(mhash) + "," + host + "," + dest + "," + mtime + "," + message

    def incoming_connection(self, source, condition):
        sock, info = self.server_sock.accept()
        address, psm = info

        self.add_text("\naccepted connection from %s" % str(address))

        # add new connection to list of peers
        self.peers[address] = sock
        self.addresses[sock] = address

        source = gobject.io_add_watch (sock, gobject.IO_IN, self.data_ready)
        self.sources[address] = source
        return True

    def incoming_connection_wifi(self, source, condition):
        sock, addr = self.server_sock_wifi.accept()

        address = addr[0]
        if not address in self.addresses:
            self.add_text("\naccepted connection from %s" % str(addr[0]))

            # add new connection to list of peers
            self.peers[address] = sock
            self.addresses[sock] = address

            source = gobject.io_add_watch (sock, gobject.IO_IN, self.data_ready)
            self.sources[address] = source
            return True

    def data_ready(self, sock, condition):
        address = self.addresses[sock]
        incoming_type = self.get_socket_type(sock)
        data = sock.recv(1023)
        print "Data:[%s]\nSocket Type:[%s]\n" % (data, incoming_type)
        if len(data) > 0:
            s_data = str(data)
            s_data_arr = s_data.split(",")

            if not s_data_arr[0].isdigit():
                self.hosts[address] = s_data_arr[0]
                self.discovered.append ((address, s_data_arr[0]))
                rows = conn.execute("SELECT * FROM messages WHERE dest=\"" + s_data_arr[0] + "\"")
                for row in rows:
                    sock.send(self.get_data(row[0], row[1], row[2], row[3], row[4]))
                    print self.get_data(row[0], row[1], row[2], row[3], row[4])
                    print "Queued message [%s] sent." % row[4]
                print self.hosts
                if s_data_arr[1] == "1":
                    sock.send(self.hostname + ",2")
                return True

            mhash = s_data_arr[0]
            name = s_data_arr[1]
            dest = s_data_arr[2]
            mtime = s_data_arr[3]
            message = ",".join(s_data_arr[4:])

            if dest == "" or dest == self.hostname:
                self.add_text("\n%s: %s" % (name, message))
                if dest == self.hostname:
                    return True

            if dest in self.hosts:
                keys = self.hosts.keys()
                values = self.hosts.values()
                sock = self.peers[keys[values.index(dest)]]
                sock.send(data)
                "Data sent to that host"
                return True
            else:
                conn.execute("INSERT INTO messages VALUES (?, ?, ?, ?, ?)", mhash, host, dest, mtime, message)
                print "Messaged added to queue"
                conn.commit()
            if s_data not in self.messages:
                self.messages.append(s_data)
                for addr, sock in list(self.peers.items()):
                    if addr != address:
                        sock_type = self.get_socket_type(sock)
                        if incoming_type == "wifi":
                            if sock_type == "wifi":
                                continue
                        sock.send(data)
        else:
            self.add_text("\nlost connection with %s" % address)
            gobject.source_remove(self.sources[address])
            del self.sources[address]
            del self.peers[address]
            del self.addresses[sock]
            for row in self.discovered:
                if row[0] == address:
                    self.discovered.remove(row.iter)
                    break
            sock.close()
            
        return True

# --- other stuff

    def get_socket_type(self, sock):
        socket_type = str(type(sock))
        if socket_type == "<class 'socket._socketobject'>":
            return "wifi"
        else:
            return "bluetooth"

    def cleanup(self):
        self.hci_sock.close()

    def connect(self, addr, name):
        sock = bluetooth.BluetoothSocket (self.bluetoothConnType)
        sock.settimeout(self.timeout)
        try:
            sock.connect((addr, self.bluetoothPort))
            sock.send(self.hostname + ",1")
        except Exception as e:
            template = "An exception of type {0} occured. Arguments:{1!r}"
            mesg = template.format(type(e).__name__, e.args)
            print mesg
            sock.close()
            return

        self.peers[addr] = sock
        self.hosts[sock] = name
        source = gobject.io_add_watch (sock, gobject.IO_IN, self.data_ready)
        self.sources[addr] = source
        self.addresses[sock] = addr


    def add_text(self, text):
        self.text_buffer.insert(self.text_buffer.get_end_iter(), text)

    def start_server(self):
        self.server_sock = bluetooth.BluetoothSocket (self.bluetoothConnType)
        self.server_sock.bind(("",self.bluetoothPort))
        self.server_sock.listen(1)

        gobject.io_add_watch(self.server_sock, gobject.IO_IN, self.incoming_connection)

        if self.wifi:
            self.server_sock_wifi = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_sock_wifi.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_sock_wifi.bind((self.server_IP, 12345))
            self.server_sock_wifi.listen(5)

            gobject.io_add_watch(self.server_sock_wifi, gobject.IO_IN, self.incoming_connection_wifi)

    def run(self):
        self.text_buffer.insert(self.text_buffer.get_end_iter(), "loading..")
        self.start_server()
        gtk.main()

    def discover(self, IP):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3.0)

        server_address = (IP, self.wifi_port)

        try:
            sock.connect(server_address)
            sock.send(self.hostname + ",1")
            self.peers[IP] = sock
            source = gobject.io_add_watch (sock, gobject.IO_IN, self.data_ready)
            
            self.sources[IP] = source
            self.addresses[sock] = IP
        except Exception as e:
            template = "An exception of type {0} occured. Arguments:{1!r}"
            mesg = template.format(type(e).__name__, e.args)
            #print mesg

    def discover_bluetooth(self, addr, name):
        try:
            print "Trying to connect %s" %  name
            self.connect(addr, name)
        except Exception as e:
            template = "An exception of type {0} occured. Arguments:{1!r}"
            mesg = template.format(type(e).__name__, e.args)
            print mesg

if __name__ == "__main__":
    gui = BluezChatGui()
    gui.run()
