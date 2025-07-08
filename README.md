# Running this

Please visit https://blog.talktech.info/home/perfecting-a-pimoroni-presto-project for all the information

## Getting the code to the Presto:

Save the presto code to your Presto using a tool like Thonny. Save the file as main.py if you would like to to run on startup of the device.
    
## Running the PC server code:

Clone the following repository and follow the instructions:
<pre language-bash>
<code>git clone https://github.com/vwillcox/PrestoMediaPlaying.git
cd PrestoMediaPlaying
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt</code>
</pre>
Now if you just want to test this you can run in debug mode:
<pre language-bash>
<code>python3 media-server.py</code>
</pre>

Now install the Presto Code to your Presto using Thonny and run
Play some media on your PC (Youtube, Spotify etc) and the item should show on your Presto.
If it does not you need to install one more component

#### ARCH Based Linux
<pre language-bash>
<code>sudo pacman -S playerctl</code>
</pre>
#### Debian Based Linux
<pre language-bash>
<code>sudo apt install -y playerctl</code>
</pre>

and now ensure it is running:
<pre language-bash>
<code>playerctld daemon</code>
</pre>

If all is working and you want to run the server code in a production environment, there is one more step

<pre language-bash>
<code>playerctld daemon
export FLASK_ENV=production
export FLASK_APP=media-server.py
gunicorn media-server:app --bind 0.0.0.0:5000 --daemon</code>
</pre>
