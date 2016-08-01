import os
import sys
import time
import threading
import socket
import urllib2

try:
    import gtk
    import gobject
    import gtk.glade
except:
    print "Please install gtk, gobject and glade packages for Python, exiting."
    sys.exit()

try:
    import bluetooth
    bluetoothAvailability = True
except:
    bluetoothAvailability = False
    print "I can\'t use bluetooth in your system, sorry mate :("

GLADEFILE="bluezchat.glade"

wifi_availability = True
bluetoothAvailability = True

# *****************

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
                "on_chat_button_clicked" : self.chat_button_clicked,
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
        self.chat_button = self.main_window_xml.get_widget("chat_button")
        self.send_button = self.main_window_xml.get_widget("send_button")
        self.main_text = self.main_window_xml.get_widget("main_text")
        self.text_buffer = self.main_text.get_buffer()

        self.input_tb = self.main_window_xml.get_widget("input_tb")

        self.listed_devs = []

        self.chat_button.set_sensitive(False)

        self.peers = {}
        self.sources = {}
        self.addresses = {}
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
            self.server_IP = str([(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])
            self.server_IP_template = self.server_IP[:9]
            self.wifi_port = 12345
        self.bluetooth = bluetoothAvailability

# --- gui signal handlers

    def quit_button_clicked(self, widget):
        gtk.main_quit()

    def scan_button_clicked(self, widget):
        self.quit_button.set_sensitive(False)
        self.scan_button.set_sensitive(False)

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
            self.discovered.clear()
            for addr, name in bluetooth.discover_devices (lookup_names = True):
                self.discovered.append ((addr, name))
        else:
            print "Bluetooth scan skipped, no bluetooth module found."

        self.quit_button.set_sensitive(True)
        self.scan_button.set_sensitive(True)

        print "Done"

    def send_button_clicked(self, widget):
        text =  str(int(time.time()) % 1000) + "," + self.hostname + "," + self.input_tb.get_text()
        if len(text) == 0: return

        for addr, sock in list(self.peers.items()):
            try:
                sock.send(text)
                print "sent to ", sock
            except:
                continue

        self.input_tb.set_text("")
        s_data_arr = text.split(",")
        message = s_data_arr[2]
        self.add_text("\n%s: %s" % (self.hostname, message))

    def chat_button_clicked(self, widget):
        (model, iter) = self.devices_tv.get_selection().get_selected()
        if iter is not None:
            addr = model.get_value(iter, 0)
            if addr not in self.peers:
                self.add_text("\nconnecting to %s" % addr)
                self.connect(addr)
            else:
                self.add_text("\nAlready connected to %s!" % addr)

    def devices_tv_cursor_changed(self, widget):
        (model, iter) = self.devices_tv.get_selection().get_selected()
        if iter is not None:
            self.chat_button.set_sensitive(True)
        else:
            self.chat_button.set_sensitive(False)

# --- network events

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
            name = s_data_arr[1]
            message = s_data_arr[2]
            self.add_text("\n%s: %s" % (name, message))
            if s_data not in self.messages:
                self.messages.append(s_data)
                for addr, sock in list(self.peers.items()):
                    print "addr: %s, sock: %s" % (addr, sock)
                    print "address = %s" % address
                    if addr != address:
                        print "address doesnt match"
                        sock_type = self.get_socket_type(sock)
                        print "sock type: %s" % sock_type
                        if incoming_type == "wifi":
                            if sock_type == "wifi":
                                continue
                        sock.send(s_data)
        else:
            self.add_text("\nlost connection with %s" % address)
            gobject.source_remove(self.sources[address])
            del self.sources[address]
            del self.peers[address]
            del self.addresses[sock]
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

    def connect(self, addr):
        sock = bluetooth.BluetoothSocket (bluetooth.L2CAP)
        try:
            sock.connect((addr, 0x1001))
        except bluez.error as e:
            self.add_text("\n%s" % str(e))
            sock.close()
            return

        self.peers[addr] = sock
        source = gobject.io_add_watch (sock, gobject.IO_IN, self.data_ready)
        self.sources[addr] = source
        self.addresses[sock] = addr


    def add_text(self, text):
        self.text_buffer.insert(self.text_buffer.get_end_iter(), text)

    def start_server(self):
        self.server_sock = bluetooth.BluetoothSocket (bluetooth.L2CAP)
        self.server_sock.bind(("",0x1001))
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
            #sock.send("4878,ali-pc,asdasd")
            print server_address
            self.peers[IP] = sock
            source = gobject.io_add_watch (sock, gobject.IO_IN, self.data_ready)
            
            self.sources[IP] = source
            self.addresses[sock] = IP
        except Exception as e:
            template = "An exception of type {0} occured. Arguments:{1!r}"
            mesg = template.format(type(e).__name__, e.args)
            #print mesg

if __name__ == "__main__":
    gui = BluezChatGui()
    gui.run()