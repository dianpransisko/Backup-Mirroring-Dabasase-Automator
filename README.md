# 🚀 Enterprise PostgreSQL Backup & Mirroring Automator


A robust, Python-powered automation suite designed to secure enterprise database environments and streamline analytical workflows. This project bridges the gap between **Production Data Security** and **Data Analytics Accessibility**.

## 🌟 Key Features

* **Automated Scheduling**: Hands-free daily backups integrated with Windows Task Scheduler.
* **Database Mirroring**: Automatic synchronization from Production (ERP) to an isolated Mirror DB to protect server performance during heavy analytical queries.
* **Secure Credential Management**: Implementation of `.env` patterns to ensure no sensitive credentials (passwords/host) are hardcoded.
* **Real-time Alerts**: Instant email notifications (via SMTP) providing success/failure reports directly to the administrator.
* **One-Click Manual Trigger**: Custom Batch (`.bat`) scripts for instant backups and mirror refreshes, designed for non-technical team members (Data Analysts).
* **Auto-Cleanup**: Intelligent storage management that removes outdated backups to optimize disk space.

## 🏗️ System Architecture

The system follows a modular architecture to ensure high availability and data integrity:
1. **Source**: PostgreSQL Production Database (ERP).
2. **Process**: Python script executes `pg_dump` and manages error handling.
3. **Storage**: Secure local directory with timestamped `.sql` files.
4. **Mirroring**: Automated `DROP/CREATE/RESTORE` cycle to a secondary "Analyst-Ready" database.
5. **Notification**: SMTP gateway sends detailed logs to the IT/Data team.



## 🛠️ Tech Stack

* **Language**: Python 3.10+
* **Database**: PostgreSQL
* **Libraries**: `psycopg2`, `python-dotenv`, `smtplib`
* **Automation**: Windows Task Scheduler & Batch Scripting

## 🚀 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/yourusername/pg-backup-mirror.git](https://github.com/yourusername/pg-backup-mirror.git)