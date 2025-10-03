- Run `sudo systemctl start teradata_np_mcp.service` to start the service.
- Run `sudo systemctl status teradata_np_mcp.service` to check status.
- Run `sudo systemctl enable teradata_np_mcp.service` to enable start on system boot.
- To be safe, test increasing restart intervals for stability. Create a crontab for the service:
    - Run `sudo crontab -e`
    - Add the following line:
      ```
      0 * * * * /bin/systemctl restart teradata_np_mcp.service