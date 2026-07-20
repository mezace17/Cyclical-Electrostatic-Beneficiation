### Written by Elizabeth Romero
library(ggplot2)
install.packages("fields")
library(fields)
library(MASS)
library(car)

### Import data - INSERT DIRECTORY
raw_data <- read.csv(f'{insert directory here}', 
                 header=TRUE, colClasses = c("numeric","factor","numeric","numeric"))

## DIAGNOSTIC RESIDUAL PLOTS
diagnostic_fit <- lm(Data ~ Voltage * Run * Puck, data=raw_data)
stud_dia <-residuals(diagnostic_fit)/sd(residuals(diagnostic_fit))

# residual plot
ggplot(raw_data, aes(x = fitted(diagnostic_fit), y = residuals(diagnostic_fit)/sd(residuals(diagnostic_fit)))) +
  geom_point() +
  geom_hline(yintercept = 0, color = "magenta", linetype = "dashed") +
  ggtitle("Semi-Studentized Residuals vs Fitted Values") +
  xlab("Fitted Values") +
  ylab("Semi-Studentized Residuals")

# linear regression
plot(raw_data$Voltage, raw_data$Data, main = "Simple Linear Regression of % Weight of Titanium and Voltage Level", xlab = "Voltage (V)", ylab = "% Titanium")
abline(diagnostic_fit)
summary(diagnostic_fit)

# Q-Q plot
fitted_values <- fitted(diagnostic_fit)
residuals <- residuals(diagnostic_fit)
residual_std <- sd(residuals)
semi_studentized <- residuals / residual_std
raw_data$residuals_clean <- residuals
raw_data$fitted_values_clean <- fitted_values
raw_data$semi_studentized_residuals_clean <- semi_studentized
qqnorm(residuals(raw_data))
qqline(residuals(raw_data), col = "red")

## Remove outliers and zeros from data
cleaned_data <- subset(raw_data, abs(residuals(diagnostic_fit)/sd(residuals(diagnostic_fit))) <= 3&raw_data$Data!=0)
cleaned_aov <- aov(Data ~ Voltage * Run * Puck, data=cleaned_data)
cleaned_lm <- lm(Data ~ Voltage * Run * Puck, data=cleaned_data)

plot(cleaned_data$Voltage, cleaned_data$Data, main = "Simple Linear Regression of % Weight of Titanium and Voltage Level", xlab = "Voltage (V)", ylab = "% Titanium")
abline(cleaned_lm)
summary(cleaned_lm)

stud_cleaned <-residuals(cleaned_aov)/sd(residuals(cleaned_aov))

fitted_values <- fitted(cleaned_lm)
residuals <- residuals(cleaned_lm)
residual_std <- sd(residuals)
semi_studentized <- residuals / residual_std

# Plot studentized residuals 
ggplot(cleaned_data, aes(x = fitted(cleaned_aov), y = stud_cleaned)) +
  geom_point() +
  geom_hline(yintercept = 0, color = "red", linetype = "dashed") +
  ggtitle("Semi-Studentized Residuals vs Fitted Values (After Removing Outliers)") +
  xlab("Fitted Values") +
  ylab("Semi-Studentized Residuals")

# SAME as above Plot studentized residuals 
ggplot(cleaned_data, aes(x = fitted(cleaned_aov), y = semi_studentized)) +
  geom_point() +
  geom_hline(yintercept = 0, color = "green", linetype = "dashed") +
  ggtitle("Semi-Studentized Residuals vs Fitted Values (After Removing Outliers)") +
  xlab("Fitted Values") +
  ylab("Semi-Studentized Residuals")

# Plot absolute residuals
ggplot(cleaned_data, aes(x = fitted(cleaned_aov), y = abs(stud_cleaned))) +
  geom_point() +
  geom_smooth(method = "lm", color = "blue", se = FALSE) +
  ggtitle("Absolute Value of Residuals vs Fitted Values") +
  xlab("Fitted Values") +
  ylab("Absolute Value of Semi-Studentized Residuals")

# Check for normality 
shapiro.test(stud_cleaned)
shapiro.test(semi_studentized)

# Spearman rank correlation test
cor_test <- cor.test(abs(semi_studentized_residuals_clean), fitted_values_clean, method = "spearman")

# Q-Q plot
cleaned_data$residuals_clean <- residuals
cleaned_data$fitted_values_clean <- fitted_values
cleaned_data$semi_studentized_residuals_clean <- semi_studentized
qqnorm(residuals(cleaned_data))
qqline(residuals(cleaned_data), col = "red")

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

anova_model <- aov(Ti_val ~ volt * run * puck, data = data_clean)
summary(anova_model)

TukeyHSD(anova_model)

