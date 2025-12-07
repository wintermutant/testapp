# Deployment Instructions for Raspberry Pi

## Prerequisites
- Raspberry Pi with static IP: 192.168.4.50
- SSH access to the Pi
- nginx already installed and running

## Step 1: Copy files to Raspberry Pi

From your Mac, in the testapp directory:

```bash
scp -r . pi@192.168.4.50:~/testapp
```

Replace `pi` with your actual username on the Raspberry Pi.

## Step 2: SSH into your Raspberry Pi

```bash
ssh pi@192.168.4.50
```

## Step 3: Install Docker (if not already installed)

```bash
sudo apt update
sudo apt install docker.io docker-compose -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
```

After running these commands, log out and log back in for group changes to take effect.

## Step 4: Start the Flask app and MongoDB

```bash
cd ~/testapp
docker-compose up -d --build
```

The `-d` flag runs containers in the background.

Verify containers are running:
```bash
docker-compose ps
```

## Step 5: Configure nginx as reverse proxy

1. **Copy the nginx configuration:**
   ```bash
   sudo cp ~/testapp/nginx.conf /etc/nginx/sites-available/flask-app
   ```

2. **Remove the default nginx site:**
   ```bash
   sudo rm /etc/nginx/sites-enabled/default
   ```

3. **Enable your Flask app site:**
   ```bash
   sudo ln -s /etc/nginx/sites-available/flask-app /etc/nginx/sites-enabled/
   ```

4. **Test nginx configuration:**
   ```bash
   sudo nginx -t
   ```

5. **Reload nginx:**
   ```bash
   sudo systemctl reload nginx
   ```

## Step 6: Access your app

From any device on your network, go to:
```
http://192.168.4.50
```

You should see your Hello App!

## Useful Commands

**View Flask app logs:**
```bash
docker-compose logs -f web
```

**View MongoDB logs:**
```bash
docker-compose logs -f mongodb
```

**Stop the app:**
```bash
docker-compose down
```

**Restart the app:**
```bash
docker-compose restart
```

**View nginx logs:**
```bash
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

## Troubleshooting

**If the app doesn't load:**

1. Check if Docker containers are running:
   ```bash
   docker-compose ps
   ```

2. Check Flask app logs:
   ```bash
   docker-compose logs web
   ```

3. Check if nginx is running:
   ```bash
   sudo systemctl status nginx
   ```

4. Check nginx error logs:
   ```bash
   sudo tail -n 50 /var/log/nginx/error.log
   ```

5. Verify port 5000 is accessible:
   ```bash
   curl http://localhost:5000
   ```

6. Check if nginx configuration is valid:
   ```bash
   sudo nginx -t
   ```
