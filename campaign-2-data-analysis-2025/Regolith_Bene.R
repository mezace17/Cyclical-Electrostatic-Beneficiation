# Code 16.470 Project
### Written by Elizabeth Romero
library(ggplot2)

### Import data - INSERT DIRECTORY
raw_data <- read.csv(f'{insert directory here}', 
                 header=TRUE, colClasses = c("numeric","factor","numeric","numeric"))
              
# Assign columns to variables
volt <- data$Voltage
puck <- data$Puck
run <- data$Run
Ti_val <- data$Data

# Sanity Check - Histogram of Voltage
ggplot(data, aes(x = volt)) +
  geom_histogram(binwidth = 1, fill = "red", color = "black", alpha = 0.7) +
  ggtitle("Histogram of Voltage Levels (V)") +
  xlab("Voltage Level (V)") +
  ylab("Frequency")

# Histogram of Ti_val
ggplot(data, aes(x = Ti_val)) +
  geom_histogram(binwidth = 0.005, fill = "blue", color = "black", alpha = 0.7) +
  ggtitle("Histogram of % Titanium") +
  xlab("Titanium (%)") +
  ylab("Frequency")

### 1st step - looking for outliers

# Fit linear model
fit <- lm(Ti_val ~ volt)

# Calculate residuals and fitted values
fitted_values <- fitted(fit)
residuals <- residuals(fit)
residual_std <- sd(residuals)
semi_studentized <- residuals / residual_std

# Add to dataframe
data$residuals <- residuals
data$fitted_values <- fitted_values
data$semi_studentized_residuals <- semi_studentized

# Plot semi-studentized residuals
ggplot(data, aes(x = fitted_values, y = semi_studentized_residuals)) +
  geom_point() +
  geom_hline(yintercept = 0, color = "magenta", linetype = "dashed") +
  ggtitle("Semi-Studentized Residuals vs Fitted Values") +
  xlab("Fitted Values") +
  ylab("Semi-Studentized Residuals")

# Scatter plot & regression
plot(volt, Ti_val, main = "Simple Linear Regression of % Titanium and Voltage Level", xlab = "Voltage (V)", ylab = "% Titanium")
abline(fit)
summary(fit)

# Remove outliers (|r| > 4)
data_clean <- subset(data, abs(semi_studentized_residuals) <= 3)

# Reassign variables to cleaned data
volt <- data_clean$Voltage
puck <- data_clean$Puck
run <- data_clean$Run
Ti_val <- data_clean$Data
# Refit model on cleaned data
fit_clean <- lm(Ti_val ~ volt, data = data_clean)

# Plot residuals after cleaning
fitted_values_clean <- fitted(fit_clean)
residuals_clean <- residuals(fit_clean)
semi_studentized_residuals_clean <- residuals_clean / sd(residuals_clean)
# Add to dataframe
data_clean$residuals_clean <- residuals_clean
data_clean$fitted_values_clean <- fitted_values_clean
data_clean$semi_studentized_residuals_clean <- semi_studentized_residuals_clean

ggplot(data_clean, aes(x = fitted_values_clean, y = semi_studentized_residuals_clean)) +
  geom_point() +
  geom_hline(yintercept = 0, color = "red", linetype = "dashed") +
  ggtitle("Semi-Studentized Residuals vs Fitted Values (After Removing Outliers)") +
  xlab("Fitted Values") +
  ylab("Semi-Studentized Residuals")

# Plot absolute residuals
ggplot(data_clean, aes(x = fitted_values_clean, y = abs(semi_studentized_residuals_clean))) +
  geom_point() +
  geom_smooth(method = "lm", color = "blue", se = FALSE) +
  ggtitle("Absolute Value of Residuals vs Fitted Values") +
  xlab("Fitted Values") +
  ylab("Absolute Value of Semi-Studentized Residuals")

# Spearman rank correlation test
cor_test <- cor.test(abs(semi_studentized_residuals_clean), fitted_values_clean, method = "spearman")
cor_test

# Q-Q plot
qqnorm(data_clean$residuals_clean)
qqline(data_clean$residuals_clean, col = "red")

# Levene Test for Homo Variance
library(car)
leveneTest(Ti_val ~ interaction(volt,puck,run), data=data_clean)
leveneTest(Ti_val ~ volt, data=data_clean)
leveneTest(Ti_val ~ puck, data=data_clean)
leveneTest(Ti_val ~ run, data=data_clean)

# ANOVA (convert variables to factors)
data_clean$volt <- as.factor(data_clean$Voltage)
data_clean$run <- as.factor(data_clean$Run)
data_clean$puck <- as.factor(data_clean$Puck)

anova_model <- aov(Ti_val ~ volt + run + puck, data = data_clean)
summary(anova_model)

TukeyHSD(anova_model)


