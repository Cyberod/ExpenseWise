---

# Expense Tracker Dashboard

The **Expense Tracker Dashboard** is a web application designed to help users manage their personal finances by tracking expenses and income. It provides an intuitive interface for adding, editing, and deleting financial records, as well as generating insightful visualizations and exporting data in various formats.

## Features

### Expense and Income Management
- **Add, Edit, and Delete Records**: Easily manage your expenses and income with a user-friendly interface.
- **Categorization**: Organize expenses by categories and income by sources for better tracking.

### Data Visualization
- **Charts and Graphs**: View your financial data through interactive pie charts and bar charts for both expenses and income.
- **Expense and Income Summaries**: Get a breakdown of spending and income over the last six months.

### Export Options
- **Export to CSV, Excel, and PDF**: Download your financial data in multiple formats for offline use or sharing.

### Search and Pagination
- **Search Functionality**: Quickly find specific records using the search bar.
- **Paginated Views**: Navigate through your records with ease using pagination.

### Authentication and Security
- **User Authentication**: Secure login and session management to ensure data privacy.
- **Role-Based Access**: Each user can only view and manage their own financial data.

## Technology Stack
- **Backend**: Django 5.1 (Python)
- **Frontend**: HTML, CSS, Bootstrap Css, JavaScript (with Chart.js for visualizations)
- **Database**: SQLite (default, configurable for production)
- **Export Libraries**: `xlwt` for Excel, `weasyprint` for PDF generation
- **Other Tools**: Django Messages Framework for notifications, Django Paginator for record navigation

## Installation and Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd expensewebsite
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   - Create a .env file in the root directory.
   - Add the following variables:
     ```
     EMAIL_HOST=<your-email-host>
     EMAIL_PORT=<your-email-port>
     EMAIL_HOST_USER=<your-email>
     EMAIL_HOST_PASSWORD=<your-email-password>
     EMAIL_USE_TLS=True
     ```
4. Run database migrations:
   ```bash
   python manage.py migrate
   ```
5. Start the development server:
   ```bash
   python manage.py runserver
   ```
---

## Usage
- **Dashboard**: View summaries of your expenses and income.
- **Add Expense/Income**: Navigate to the respective pages to add new records.
- **Export Data**: Use the export buttons to download your data in CSV, Excel, or PDF format.
- **Visualizations**: Visit the "Stats" page to view interactive charts.

## Folder Structure
- **`expenses/`**: Handles expense-related functionality (models, views, templates).
- **`userincome/`**: Manages income-related features.
- **`dashboard/`**: Provides aggregated data and visualizations.
- **`authentication/`**: Handles user authentication and session management.
- **`userpreferences/`**: Stores user-specific preferences like currency.
- **`static/`**: Contains static files (CSS, JavaScript).
- **`templates/`**: HTML templates for rendering views.

## Screenshots
- **Dashboard**: Overview of expenses and income.
<img src="[image-url](https://github.com/user-attachments/assets/bc7e0d62-8714-4a1a-9a95-c51201678e1f)" alt="Dashboard" width="300" style="border-radius: 8px; border: 2px solid #ccc;" />
- **Add Expense**: Form to add a new expense.
- <img src="[image-url](https://github.com/user-attachments/assets/bc7e0d62-8714-4a1a-9a95-c51201678e1f)" alt="Add Expense" width="300" style="border-radius: 8px; border: 2px solid #ccc;" />
- **Expense Summary**: Interactive charts for expense distribution.
- <img src="[image-url](https://github.com/user-attachments/assets/bc7e0d62-8714-4a1a-9a95-c51201678e1f)" alt="Expense Summary" width="300" style="border-radius: 8px; border: 2px solid #ccc;" />

## Future Enhancements
- Add support for recurring expenses and income.
- Integrate additional export formats (e.g., JSON).
- Implement advanced analytics for financial forecasting.

---

## 📧 Contact

For questions or feedback, feel free to reach out:

- **Email**: jonazkeez@gmail.com
- **GitHub**: [Cyberod](https://github.com/Cyberod)
