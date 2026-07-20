### Written by Elizabeth Romero
library(ggplot2)
install.packages("fields")
library(fields)
library(MASS)
library(car)

### Import data - INSERT DIRECTORY
raw_data <- read.csv(f'{insert directory here}', 
                 header=TRUE, colClasses = c("numeric","factor","numeric","numeric"))

# Assign columns to variables
volt <- raw_data$Voltage
puck <- raw_data$Puck
run <- raw_data$Run
Ti_val <- raw_data$Data

# Sanity Check - Histogram of Voltage
ggplot(data, aes(x = volt)) +
  geom_histogram(binwidth = 1, fill = "red", color = "black", alpha = 0.7) +
  ggtitle("Histogram of Voltage Levels (V)") +
  xlab("Voltage Level (V)") +
  ylab("Frequency")

# Histogram of Fe_val
ggplot(data, aes(x = Ti_val)) +
  geom_histogram(binwidth = 0.005, fill = "blue", color = "black", alpha = 0.7) +
  ggtitle("Histogram of % Weight Titanium") +
  xlab("Titanium (%)") +
  ylab("Frequency")

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
plot(raw_data$Voltage, raw_data$Data, main = "Simple Linear Regression of % Weight of Iron and Voltage Level", xlab = "Voltage (V)", ylab = "% Titanium")
abline(diagnostic_fit)
summary(diagnostic_fit)

# Q-Q plot
fitted_values_clean <- fitted(diagnostic_fit)
residuals_clean <- residuals(diagnostic_fit)
semi_studentized_residuals_clean <- residuals_clean / sd(residuals_clean)
qqnorm(residuals_clean)
qqline(residuals_clean, col = "red")

## Remove outliers and zeros from data
cleaned_data <- subset(raw_data, abs(residuals(diagnostic_fit)/sd(residuals(diagnostic_fit))) <= 3&raw_data$Data!=0)
cleaned_aov <- aov(Data ~ Voltage * Run * Puck, data=cleaned_data)
cleaned_lm <- lm(Data ~ Voltage * Run * Puck, data=cleaned_data)

stud_cleaned <-residuals(cleaned_aov)/sd(residuals(cleaned_aov))

# Plot studentized residuals 
ggplot(cleaned_data, aes(x = fitted(cleaned_aov), y = stud_cleaned)) +
  geom_point() +
  geom_hline(yintercept = 0, color = "red", linetype = "dashed") +
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

### TRANSFORM DATA 
pt<- powerTransform(cleaned_aov, family="bcPower")
cleaned_data$transformed <- bcPower(cleaned_data$Data, pt$lambda)


cleaned_transformed_aov <- aov(transformed ~ Voltage * Run * Puck, data=cleaned_data)
cleaned_transformed_lm <- lm(transformed ~ Voltage * Run, data=cleaned_data)
residuals_transformed <- residuals(cleaned_transformed_lm)
stud_transformed <- residuals(cleaned_transformed_aov)/sd(residuals(cleaned_transformed_aov))

shapiro.test(stud_transformed)


# Plot studentized residuals of TRANSFORMED DATA
ggplot(cleaned_data, aes(x = fitted(cleaned_transformed_aov), y = stud_transformed)) +
  geom_point() +
  geom_hline(yintercept = 0, color = "red", linetype = "dashed") +
  ggtitle("Semi-Studentized Residuals vs Fitted Values (After Transformation)") +
  xlab("Fitted Values") +
  ylab("Semi-Studentized Residuals")

# Plot absolute residuals
ggplot(cleaned_data, aes(x = fitted(cleaned_transformed_aov), y = abs(stud_transformed))) +
  geom_point() +
  geom_smooth(method = "lm", color = "blue", se = FALSE) +
  ggtitle("Absolute Value of Residuals vs Fitted Values") +
  xlab("Fitted Values") +
  ylab("Absolute Value of Semi-Studentized Residuals")



# Spearman rank correlation test
cor_test <- cor.test(abs(semi_studentized_residuals_clean), fitted_values_clean, method = "spearman")

# Q-Q plot
fitted_values_clean <- fitted(cleaned_transformed_lm)
residuals_clean <- residuals(cleaned_transformed_lm)
semi_studentized_residuals_clean <- residuals_clean / sd(residuals_clean)
qqnorm(residuals_clean)
qqline(residuals_clean, col = "red")

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

