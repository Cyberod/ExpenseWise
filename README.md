---

# ExpenseWise

The **ExpenseWise** is a web application designed to help users manage their personal finances by tracking expenses and income. It provides an intuitive interface for adding, editing, and deleting financial records, as well as generating insightful visualizations and exporting data in various formats.

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
3. Set up environment variables (local development):
   - Create a `.env` file in the root directory or copy `.env.example`.
   - Add the variables required such as email configuration and any API keys.
4. Run database migrations:
   ```bash
   python manage.py migrate
   ```
5. Start the development server:
   ```bash
   python manage.py runserver
   ```

### Deploying to Render
1. **Push your code** to a GitHub/GitLab repository.
2. **Create a new Web Service** on Render, connect your repo, and select the `main` (or default) branch.
3. Ensure the build command (`pip install -r requirements.txt`) and start command
   (`gunicorn expensewebsite.wsgi:application`) are set; they are also defined in
   `render.yaml` for infrastructure-as-code deployments.
4. Add environment variables in the Render dashboard or via `render.yaml`:
   - `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS` (your render domain), etc.
   - Render will automatically provide `DATABASE_URL` when you create a MySQL
     managed database (configured in `render.yaml`).
5. After deployment completes, run one-off migrations from the Render console:
   ```bash
   render exec --service expensewise-web -- python manage.py migrate
   ```
6. Static files are collected automatically during build (via `collectstatic`).
   WhiteNoise serves them from the same web service.

Refer to [render.com/docs/deploy-python-django](https://render.com/docs/deploy-python-django)
for more details.
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
