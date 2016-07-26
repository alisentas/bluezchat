package com.example.seyfullah.airties;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.ParcelUuid;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.ProgressBar;
import android.widget.Toast;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.Set;

public class MainActivity extends AppCompatActivity {
    private BluetoothAdapter btAdapter;
    private SingBroadcastReceiver Receiver;
    ProgressBar progressBar;
    int REQUEST_ENABLE_BT = 526;
    String btAygitlar = "";
    public int cikis = 0;
    private OutputStream outputStream;
    private InputStream inStream;
    ArrayList<BluetoothDevice> devices2 = new ArrayList<BluetoothDevice>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        progressBar = (ProgressBar) findViewById(R.id.progressBar);


        //register local BT adapter
        btAdapter = BluetoothAdapter.getDefaultAdapter();
        //check to see if there is BT on the Android device at all
        if (btAdapter == null) {
            int duration = Toast.LENGTH_SHORT;
            Toast.makeText(this, "No Bluetooth on this handset", duration).show();
        }
        //let's make the user enable BT if it isn't already
        if (!btAdapter.isEnabled()) {
            Intent enableBT = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
            startActivityForResult(enableBT, REQUEST_ENABLE_BT);
        }
;
        //cancel any prior BT device discovery
        if (btAdapter.isDiscovering()) {
            btAdapter.cancelDiscovery();
        }
        //re-start discovery

        Log.i("Discovery", "Starting discovery");
        btAdapter.startDiscovery();

        //let's make a broadcast receiver to register our things
        Receiver = new SingBroadcastReceiver();
        IntentFilter ifilter = new IntentFilter(BluetoothDevice.ACTION_FOUND);
        this.registerReceiver(Receiver, ifilter);
    }


    private class SingBroadcastReceiver extends BroadcastReceiver {
        public void onReceive(Context context, Intent intent) {
            progressBar.setVisibility(View.VISIBLE);
            String action = intent.getAction(); //may need to chain this to a recognizing function
            if (BluetoothDevice.ACTION_FOUND.equals(action)) {
                // Get the BluetoothDevice object from the Intent
                BluetoothDevice device = intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE);
                // Add the name and address to an array adapter to show in a Toast
                btAygitlar = device.getName() + "    " + device.getAddress();
                devices2.add(device);
                /*try {
                    init();
                    write("denemeee");

                    run();
                    Toast.makeText(getApplicationContext(), devices2.get(2).getName() + "  gonderildi", Toast.LENGTH_LONG).show();
                } catch (IOException e) {
                    e.printStackTrace();
                }*/
            }
            Toast.makeText(context, btAygitlar, Toast.LENGTH_LONG).show();
            progressBar.setVisibility(View.GONE);

        }
    }

    /*public void write(String s) throws IOException {
        outputStream.write(s.getBytes());
    }*/

    /*private void init() throws IOException {
        BluetoothAdapter blueAdapter = BluetoothAdapter.getDefaultAdapter();
        if (blueAdapter != null) {
            if (blueAdapter.isEnabled()) {
                Set<BluetoothDevice> bondedDevices = blueAdapter.getBondedDevices();

                if (bondedDevices.size() > 0) {
                    Object[] devices = (Object[]) bondedDevices.toArray();
                    BluetoothDevice device = (BluetoothDevice) devices2.get(0);
                    ParcelUuid[] uuids = device.getUuids();
                    BluetoothSocket socket = device.createRfcommSocketToServiceRecord(uuids[0].getUuid());
                    socket.connect();
                    outputStream = socket.getOutputStream();
                    inStream = socket.getInputStream();
                }

                Log.e("error", "No appropriate paired devices.");
            } else {
                Log.e("error", "Bluetooth is disabled.");
            }
        }
    }*/

    /*public void run() {
        final int BUFFER_SIZE = 1024;
        byte[] buffer = new byte[BUFFER_SIZE];
        int bytes = 0;
        int b = BUFFER_SIZE;

        while (true) {
            try {
                bytes = inStream.read(buffer, bytes, BUFFER_SIZE - bytes);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }*/

}
