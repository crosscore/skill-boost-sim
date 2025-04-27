import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from matplotlib import ticker

# Default parameters (will be filled later)
PARAMS = {}

def calculate_annual_income(params):
    """Calculate annual net income for both career paths."""
    print("Calculating annual income...")

    # Extract parameters for readability
    age_start = params['age_start']
    age_end = params['age_end']

    # Office worker parameters
    office_monthly_net_salary = params['office_initial_monthly_net_salary']
    office_bonus_months = params['office_bonus_months']
    office_raise_rate = params['office_raise_rate']

    # Freelance parameters
    learning_period_months = params['freelance_learning_period_months']
    learning_period_years = learning_period_months / 12.0  # fractional years
    fl_init_wage = params['freelance_initial_hourly_wage']
    fl_target_wage = params['freelance_target_hourly_wage']
    fl_target_years = params['freelance_target_reach_years']
    fl_growth_type = params['freelance_hourly_wage_growth_type']
    fl_post_raise_rate = params['freelance_post_target_raise_rate']
    fl_hours_per_day = params['freelance_work_hours_per_day']
    fl_days_per_month = params['freelance_work_days_per_month']
    fl_expense_rate = params['freelance_expense_rate']
    fl_deduction_rate = params['deduction_rate_freelance']

    # Years array
    years = np.arange(age_start, age_end + 1)
    num_years = len(years)

    # Initialize income arrays
    income_office = np.zeros(num_years, dtype=float)
    income_freelance = np.zeros(num_years, dtype=float)

    # --- Office worker calculations ---
    current_monthly_salary = office_monthly_net_salary
    for i in range(num_years):
        # Annual net income = monthly net * 12 + bonus months * monthly net
        income_office[i] = current_monthly_salary * (12 + office_bonus_months)
        # Raise for next year
        current_monthly_salary *= (1 + office_raise_rate)

    # --- Freelance calculations ---
    for i in range(num_years):
        years_since_start = i  # integer year offset from start

        # Determine if within learning period (using simplified approach)
        if years_since_start < np.ceil(learning_period_years):
            income_freelance[i] = 0.0
            continue

        # Work years since learning completed
        work_years = years_since_start - learning_period_years

        # Determine hourly wage
        if work_years <= fl_target_years:
            # quadratic growth 0 -> 1
            ratio = (work_years / fl_target_years) ** 2 if fl_target_years > 0 else 1.0
            current_hourly_wage = fl_init_wage + (fl_target_wage - fl_init_wage) * ratio
        else:
            years_after_target = work_years - fl_target_years
            current_hourly_wage = fl_target_wage * ((1 + fl_post_raise_rate) ** years_after_target)

        # Annual gross income
        annual_gross = current_hourly_wage * fl_hours_per_day * fl_days_per_month * 12

        # Apply expenses and deductions to obtain net income
        taxable_income = annual_gross * (1 - fl_expense_rate)
        net_income = taxable_income * (1 - fl_deduction_rate)

        income_freelance[i] = net_income

    return years, income_office, income_freelance

def calculate_cumulative_income(years, income_office, income_freelance):
    """Calculate cumulative net income."""
    # TODO: Implement cumulative sum
    print("Calculating cumulative income...")
    cumulative_office = np.cumsum(income_office)
    cumulative_freelance = np.cumsum(income_freelance)
    return cumulative_office, cumulative_freelance

def plot_income_comparison(years, cumulative_office, cumulative_freelance, params):
    """Plot the cumulative income comparison graph."""
    # TODO: Implement plotting logic
    print("Plotting cumulative income...")
    output_dir = Path("./output")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "cumulative_income.png"

    plt.figure(figsize=(12, 7))
    plt.plot(years, cumulative_office, label="Office Worker (Net)")
    plt.plot(years, cumulative_freelance, label="Freelance Engineer (Net)")

    plt.xlabel("Age")
    plt.ylabel("Cumulative Net Income (JPY)")
    plt.title("Lifetime Cumulative Net Income Comparison")
    plt.legend()
    plt.grid(True)

    # Format y-axis to show full numbers, disable scientific notation and offset
    ax = plt.gca()
    formatter = ticker.ScalarFormatter(useOffset=False)
    formatter.set_scientific(False)
    ax.yaxis.set_major_formatter(formatter)

    # Adjust layout to prevent labels from being cut off
    plt.subplots_adjust(left=0.15) # Increase left margin
    plt.tight_layout() # Apply tight layout *after* adjusting margins

    # TODO: Add final total amounts and difference to the plot or title

    plt.savefig(output_path)
    print(f"Graph saved to {output_path}")

# Optional: Functions for effective hourly wage calculation and plotting
def calculate_effective_hourly_wage(params, years, income_office, income_freelance):
    """Calculate effective hourly wage for both paths."""
    # TODO: Implement calculation based on order.md
    print("Calculating effective hourly wage...")
    effective_wage_office = np.zeros_like(years, dtype=float)
    effective_wage_freelance = np.zeros_like(years, dtype=float)
    return effective_wage_office, effective_wage_freelance

def plot_effective_hourly_wage(years, wage_office, wage_freelance, params):
    """Plot the effective hourly wage comparison."""
    # TODO: Implement plotting logic
    print("Plotting effective hourly wage...")
    output_dir = Path("./output")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "effective_hourly_wage.png"

    plt.figure(figsize=(12, 7))
    plt.plot(years, wage_office, label="Office Worker (Effective Hourly)")
    plt.plot(years, wage_freelance, label="Freelance Engineer (Effective Hourly)")

    plt.xlabel("Age")
    plt.ylabel("Effective Hourly Wage (JPY)")
    plt.title("Effective Hourly Wage Comparison")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(output_path)
    print(f"Graph saved to {output_path}")


def main():
    """Main function to run the simulation."""
    # --- Parameters --- (Based on order.md, using defaults)
    params = {
        # Common
        'age_start': 22,
        'age_end': 60,
        'deduction_rate_employee': 0.2, # Example: 80% net income
        'deduction_rate_freelance': 0.25, # Example: Includes income tax, health insurance, pension etc. after expenses
        'freelance_expense_rate': 0.1, # Example: 10% of gross income as expenses

        # Case A: Office Worker
        'office_initial_monthly_net_salary': 200000, # Example JPY
        'office_bonus_months': 2.0, # Example: 2 months worth of salary
        'office_raise_rate': 0.02, # Example: 2% annual raise
        'office_commute_hours_per_day': 1.5, # Example: Round trip
        'office_preparation_hours_per_day': 1.0, # Example: Shower, makeup etc.
        'office_work_days_per_week': 5,
        'office_work_hours_per_day': 8.0,

        # Case B: Freelance Engineer
        'freelance_learning_period_months': 6, # Example: 6 months unpaid learning
        'freelance_initial_hourly_wage': 1500, # Example JPY
        'freelance_target_hourly_wage': 8000, # Example JPY
        'freelance_target_reach_years': 5, # Example: 5 years to reach target
        'freelance_hourly_wage_growth_type': 'quadratic', # Use quadratic growth initially
        'freelance_post_target_raise_rate': 0.01, # Example: 1% raise after reaching target
        'freelance_work_hours_per_day': 8.0,
        'freelance_work_days_per_month': 20.0,
        'freelance_commute_hours_per_day': 0.0, # Assuming remote work
    }

    # --- Calculations ---
    years, income_office, income_freelance = calculate_annual_income(params)
    cumulative_office, cumulative_freelance = calculate_cumulative_income(years, income_office, income_freelance)

    # --- Plotting ---
    plot_income_comparison(years, cumulative_office, cumulative_freelance, params)

    # --- Optional: Effective Hourly Wage ---
    # Uncomment below to enable effective wage calculation and plotting
    # effective_wage_office, effective_wage_freelance = calculate_effective_hourly_wage(params, years, income_office, income_freelance)
    # plot_effective_hourly_wage(years, effective_wage_office, effective_wage_freelance, params)

    print("Simulation finished.")

if __name__ == "__main__":
    main()
