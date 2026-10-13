# UIT2702 – Cloud and Distributed Computing
# Step-by-Step Guides: Experiments 5 and 6

Based on the lab manual sections for Experiments 5 and 6. Replace example IP addresses, usernames, and paths with the values from your own VMs.

---

# Experiment 5: Virtual Instances and Server Consolidation with Fault Tolerance

**Aim:** To set up virtual instances, load balancing, server consolidation, and fault tolerance to optimize resource utilization and ensure high availability in a cloud environment.

## Part 1: Virtual Instance Management

### Step 1: Clone Ubuntu virtual machines

1. Open VMware Workstation Pro 17.
2. Open the existing Ubuntu 24.04.1 LTS VM.
3. Shut down the VM before cloning, if necessary.
4. Right-click the VM and select **Manage → Clone**.
5. Follow the cloning wizard and select **Create a full clone**.
6. Create additional VMs, for example `UbuntuClone1`, `UbuntuClone2`, and `UbuntuClone3`.
7. Power on the cloned VMs and log in to Ubuntu.

For a straightforward setup, use three Ubuntu web-server VMs and one VM as the load balancer. If your computer has limited resources, HAProxy can be installed on one of the existing VMs.

### Step 2: Install Apache on each web-server VM

Run these commands on every web-server VM:

```bash
sudo apt update
sudo apt install apache2 -y
sudo systemctl enable apache2
sudo systemctl status apache2
```

Look for `Active: active (running)`. If Apache is not running, start it:

```bash
sudo systemctl start apache2
```

### Step 3: Customize each server's web page

On the first web-server VM, run:

```bash
sudo nano /var/www/html/index.html
```

Replace the page contents with:

```html
<!DOCTYPE html>
<html>
<head>
    <title>VM 1</title>
</head>
<body>
    <h1>Welcome to Web Server 1</h1>
</body>
</html>
```

Save with `Ctrl+O`, press `Enter`, then exit with `Ctrl+X`.

Repeat on the other VMs, changing the heading to `Web Server 2` and `Web Server 3`. Then restart Apache on each VM:

```bash
sudo systemctl restart apache2
```

### Step 4: Find the VM IP addresses

Run on each VM:

```bash
ip addr
```

To use `ifconfig` as shown in the manual, install it first:

```bash
sudo apt install net-tools -y
ifconfig
```

Record the IPv4 addresses of all web servers and the load-balancer VM. The following addresses are examples only:

| Machine | Example IP |
|---|---|
| Web Server 1 | `192.168.119.128` |
| Web Server 2 | `192.168.119.129` |
| Web Server 3 | `192.168.119.130` |
| Load Balancer | `192.168.119.131` |

Test connectivity between VMs:

```bash
ping -c 4 <OTHER_VM_IP>
```

Replace the placeholder with another VM's actual IP address.

### Step 5: Test each Apache server

From a browser, open:

```text
http://<VM1_IP>
http://<VM2_IP>
http://<VM3_IP>
```

You should see the distinct page configured on each server. If a page fails to load, check the IP address, Apache status, and VM network connectivity.

## Part 2: Basic Load Balancing with HAProxy

### Step 6: Install HAProxy

On the VM selected as the load balancer, run:

```bash
sudo apt update
sudo apt install haproxy -y
```

### Step 7: Configure HAProxy

Open the configuration file:

```bash
sudo nano /etc/haproxy/haproxy.cfg
```

Append this configuration to the end of the file:

```text
frontend http_front
    bind *:80
    default_backend http_back

backend http_back
    balance roundrobin
    server vm1 <VM1_IP>:80 check
    server vm2 <VM2_IP>:80 check
    server vm3 <VM3_IP>:80 check
```

Replace each `<VM*_IP>` placeholder with the corresponding web-server IP address. If using only two web servers, remove the third `server` line.

- `frontend http_front` receives incoming HTTP requests.
- `bind *:80` listens on port 80.
- `default_backend http_back` sends requests to the backend pool.
- `balance roundrobin` distributes requests in rotation.
- `check` enables backend health checks.

Save with `Ctrl+O`, `Enter`, and `Ctrl+X`.

### Step 8: Validate and start HAProxy

Check the configuration:

```bash
sudo haproxy -c -f /etc/haproxy/haproxy.cfg
```

If the configuration is valid, restart and enable the service:

```bash
sudo systemctl restart haproxy
sudo systemctl enable haproxy
sudo systemctl status haproxy
```

Confirm that the service is `active (running)`.

### Step 9: Test load balancing

Open the following URL in a browser:

```text
http://<LOAD_BALANCER_IP>
```

Refresh several times. If each backend has different page content, requests should be distributed among healthy servers. Browser connection reuse or caching can make the page appear unchanged on some refreshes.

You can also run:

```bash
curl http://<LOAD_BALANCER_IP>
```

If it fails, check the HAProxy configuration, backend IPs, Apache status, and network connectivity.

## Part 3: Server Consolidation

### Step 10: Review VMs and identify workloads

1. Open VMware Workstation and inspect each VM.
2. Open **Edit virtual machine settings** to review memory, processor, and storage allocations.
3. Identify VMs with low usage or redundant workloads.
4. Choose a target VM with enough CPU, memory, and storage for the workloads being combined.

### Step 11: Adjust VM resources

1. Shut down the VM if required before changing hardware allocations.
2. Select the VM and open **Edit virtual machine settings**.
3. Adjust **Memory** and **Processors** as appropriate.
4. Avoid allocating more resources than the physical host can support.

### Step 12: Migrate services to the target VM

For each workload to consolidate:

1. Copy the required application files and configuration to the target VM.
2. Install the necessary software on the target.
3. Start the services on the target VM.
4. Verify that the services work and are reachable over the network.
5. Check CPU and memory utilization.

For example, if moving a web service, ensure Apache is installed and the web files are present on the target before retiring the original VM.

### Step 13: Power off unused VMs

After verifying that the migrated services work:

1. Shut down the original VMs whose workloads have been migrated.
2. Confirm that the services still work on the consolidated VM.
3. Remove unused VMs from VMware only if they are no longer required.

**Do not delete a VM until its required data and services have been migrated and verified.**

### Step 14: Check resource utilization

Run on the consolidated Ubuntu VM:

```bash
top
```

Optional interactive alternative:

```bash
sudo apt install htop -y
htop
```

Verify that the consolidated VM can handle the combined workloads without excessive CPU or memory usage.

## Part 4: Fault Tolerance

### Step 15: Create a backup clone

1. Select a critical VM in VMware.
2. Choose **VM → Manage → Clone**.
3. Select **Create a full clone**.
4. Name the clone, for example `UbuntuBackup`.
5. Complete the cloning process.

### Step 16: Synchronize files using rsync

On the backup VM, ensure SSH is installed and running:

```bash
sudo apt update
sudo apt install openssh-server -y
sudo systemctl enable --now ssh
```

On the primary VM, install rsync:

```bash
sudo apt install rsync -y
```

Create sample data on the primary VM:

```bash
mkdir -p ~/lab-data
echo "Fault tolerance test" > ~/lab-data/test.txt
```

Synchronize it to the backup VM:

```bash
rsync -av ~/lab-data/ <USERNAME>@<BACKUP_VM_IP>:/home/<USERNAME>/lab-data/
```

Replace `<USERNAME>` and `<BACKUP_VM_IP>` with the backup VM's actual username and IP. Confirm that the file exists on the backup VM.

### Step 17: Take a VMware snapshot

1. Select the critical VM.
2. Open **VM → Snapshot → Take Snapshot**.
3. Name it `Pre-Consolidation Snapshot`.
4. Complete the operation.

Snapshots help revert a VM to a previous state, but they are not a substitute for independent backups.

### Step 18: Demonstrate recovery

1. Confirm that the primary VM's service works.
2. Confirm that the backup has the synchronized data.
3. Stop the primary service or shut down the primary VM.
4. Start the service on the backup VM if required.
5. Verify that the backup service and data are accessible.

This is a manual recovery demonstration. A clone alone does not provide automatic failover.

### Result

Virtual instances were created and configured, Apache web servers were deployed, HAProxy load balancing was implemented, server consolidation was demonstrated, and backup/snapshot mechanisms were prepared for fault tolerance.

---

# Experiment 6: Task Scheduling and Load Balancing in a Cloud Environment

**Aim:** To automate task scheduling and implement load balancing in a cloud environment for efficient resource management and high availability.

## Part 1: Task Scheduling Using Cron

### Step 1: Start Ubuntu

1. Open VMware Workstation Pro 17.
2. Power on an Ubuntu VM.
3. Log in and open a terminal.

### Step 2: Create the script

Create `script.sh`:

```bash
nano script.sh
```

Enter:

```bash
#!/bin/bash
echo "Hello Selcia"
```

Save with `Ctrl+O`, press `Enter`, and exit with `Ctrl+X`.

### Step 3: Make the script executable

```bash
chmod +x script.sh
pwd
```

Note the directory printed by `pwd`. For example, `/home/selcia` means the full script path is `/home/selcia/script.sh`.

### Step 4: Schedule the script with cron

Open the crontab editor:

```bash
crontab -e
```

Add the following line, replacing `/home/selcia` with your actual directory:

```cron
*/1 * * * * /home/selcia/script.sh >> /home/selcia/output.log 2>&1
```

Save and exit.

The five timing fields represent minute, hour, day of month, month, and day of week. `*/1 * * * *` runs the command every minute. Output is appended to `output.log`.

Absolute paths are recommended because cron may not use the directory in which you created the script.

### Step 5: Verify the scheduled task

Check cron's status:

```bash
sudo systemctl status cron
```

If necessary, start and enable it:

```bash
sudo systemctl enable --now cron
```

Wait at least one minute, then inspect the output:

```bash
cat output.log
```

Expected output:

```text
Hello Selcia
Hello Selcia
```

To watch the file update:

```bash
tail -f output.log
```

Press `Ctrl+C` to stop watching.

You can inspect cron activity using:

```bash
sudo tail -f /var/log/syslog | grep CRON
```

Check the scheduled entries with:

```bash
crontab -l
```

After the experiment, remove the cron entry using `crontab -e` so it does not keep running every minute.

## Part 2: Load Balancing with HAProxy

### Step 6: Prepare backend web servers

On every backend VM, run:

```bash
sudo apt update
sudo apt install apache2 -y
sudo systemctl enable --now apache2
```

Find each backend IP:

```bash
ip addr
```

Test the servers directly:

```bash
curl http://<VM1_IP>
curl http://<VM2_IP>
curl http://<VM3_IP>
```

Replace placeholders with actual addresses. Each backend should return its configured web page.

### Step 7: Install HAProxy

On the load-balancer VM:

```bash
sudo apt update
sudo apt install haproxy -y
```

### Step 8: Configure the backend pool

Open:

```bash
sudo nano /etc/haproxy/haproxy.cfg
```

Append:

```text
frontend http_front
    bind *:80
    default_backend http_back

backend http_back
    balance roundrobin
    server vm1 <VM1_IP>:80 check
    server vm2 <VM2_IP>:80 check
    server vm3 <VM3_IP>:80 check
```

Replace the placeholders with actual backend IP addresses. Remove the third server entry if using only two backends.

### Step 9: Start and enable HAProxy

Validate the configuration:

```bash
sudo haproxy -c -f /etc/haproxy/haproxy.cfg
```

Then run:

```bash
sudo systemctl restart haproxy
sudo systemctl enable haproxy
sudo systemctl status haproxy
```

Confirm the service is `active (running)`.

### Step 10: Test the load balancer

Open:

```text
http://<LOAD_BALANCER_IP>
```

Or run:

```bash
curl http://<LOAD_BALANCER_IP>
```

Repeat the request. Distinct backend pages help demonstrate round-robin distribution. Connection reuse or browser caching can make the same page appear more than once.

If the URL fails, check HAProxy's status, backend IP addresses, Apache services, and VM network connectivity.

## Part 3: Advanced Scheduling and Prioritization (Optional)

### Step 11: Create a CPU-oriented script

Create `script1.sh`:

```bash
nano script1.sh
```

Add:

```bash
#!/bin/bash
echo "Running CPU-intensive task in script 1"
for i in {1..10000}; do
    echo -n ""
done
```

Save and exit.

### Step 12: Create a lightweight logging script

Create `script2.sh`:

```bash
nano script2.sh
```

Add the following, replacing `/home/selcia` with your actual home directory:

```bash
#!/bin/bash
echo "Logging system information in script 2"
date >> /home/selcia/system_info.log
```

Save and exit.

### Step 13: Make both scripts executable

```bash
chmod +x script1.sh script2.sh
```

### Step 14: Schedule the scripts with different nice values

Open the crontab:

```bash
crontab -e
```

Add these lines, replacing example paths with your actual absolute paths:

```cron
*/1 * * * * nice -n 10 /home/selcia/script1.sh >> /home/selcia/output-pr.log 2>&1
*/1 * * * * nice -n 5 /home/selcia/script2.sh >> /home/selcia/output-pr.log 2>&1
```

Save and exit.

A higher nice value means lower CPU scheduling priority relative to competing processes. Typical values range from `-20` (highest priority) through `0` (default) to `19` (lowest priority). Assigning different nice values does not guarantee a specific order of execution.

### Step 15: Verify the output

Wait for the scheduled jobs to run, then execute:

```bash
cat output-pr.log
```

Expected messages include:

```text
Running CPU-intensive task in script 1
Logging system information in script 2
```

The order may vary. Check cron activity if no output appears:

```bash
sudo tail -f /var/log/syslog | grep CRON
```

After testing, remove the optional cron entries using `crontab -e`.

### Result

Task scheduling was implemented using cron, HAProxy was configured to distribute HTTP requests among multiple web servers, and the optional section demonstrated how `nice` values assign different CPU scheduling priorities to tasks.

---

# Final Checklist

## Experiment 5
- [ ] Clone and start Ubuntu VMs.
- [ ] Install Apache on each web-server VM.
- [ ] Customize web pages and record VM IP addresses.
- [ ] Configure and test HAProxy.
- [ ] Review VM resource allocations and consolidate a workload.
- [ ] Create a backup clone and synchronize files with rsync.
- [ ] Take a VMware snapshot and demonstrate recovery.

## Experiment 6
- [ ] Create `script.sh` and make it executable.
- [ ] Schedule it using cron and verify `output.log`.
- [ ] Configure HAProxy and test the backend servers.
- [ ] Create the optional priority scripts.
- [ ] Verify `output-pr.log`.
- [ ] Remove cron jobs after completing the experiment.

**Practical note:** IP addresses and usernames in this guide are examples. Always use the values configured on your own VMs.
