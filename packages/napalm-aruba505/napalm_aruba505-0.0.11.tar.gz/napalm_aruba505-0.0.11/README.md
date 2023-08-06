<!DOCTYPE html>


<h2>Napalm-aruba505 </h2>

<h1></h1>

<h4>Driver implementation for Aruba OS Access Points</h4>

<p></p>

<h4>Currently supported Napalm methods:</h4>
<ul>
    <li>get_config() </li>
</ul>

<h1></h1>

<p>How to install</p>


<ul>pip install napalm-aruba505</ul>


<h3>How to use it</h3>
<ul>
    <li>import napalm</li>
    <li>from napalm import get_network_driver</li>
    <li>driver = napalm.get_network_driver("napalm_aruba505")</li>
    <li>device = driver("my-ap-1", "my_username", "my_password")</li>
    <li>config = device.get_config()<li>
    <li>print(config)</li>
</ul>



<p></p>

<h1></h1>
