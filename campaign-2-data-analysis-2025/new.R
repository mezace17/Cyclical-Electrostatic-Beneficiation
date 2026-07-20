library(ggplot2)
library(fields)
library(MASS)
library(car)
library(ez)

### Import data - INSERT DIRECTORY
raw_data <- read.csv(f'{insert directory here}', 
                 header=TRUE, colClasses = c("numeric","factor","numeric","numeric"))
                 
## DIAGNOSTIC RESIDUAL PLOTS
diagnostic_fit <- lm(Data ~ Voltage * Run * Puck, data=raw_data)
stud_dia <-residuals(diagnostic_fit)/sd(residuals(diagnostic_fit))

# diagnostic boxplot
library(dplyr)
ggplot(raw_data, aes(x = factor(Voltage), y = Data, fill = factor(Run))) +
  geom_boxplot()+
  labs(x = "Voltage", y = "Iron % Weight", fill = "Runs") +
  scale_y_continuous(labels = function(x) paste0(round(x * 100, 1), "%"),
                     limits = c(0, 0.15)
  )+# Set the max y-axis limit to 15% (0.05 is 5%))+
  scale_fill_manual(
    values = c("1" = "grey80", "2" = "grey50", "3" = "grey20")
  ) +
  theme_minimal()+
  ggtitle("Iron % Weight by Voltage and Runs")

#diagnostic histogram
ggplot(raw_data, aes(x = Data)) +
  geom_histogram(binwidth = 0.005, fill = "blue", color = "black", alpha = 0.7) +
  ggtitle("Histogram of % Titanium") +
  xlab("Titanium (%)") +
  ylab("Frequency")

#diagnostic bar chart
ggplot(raw_data, aes(x = factor(Voltage), y = Data, fill = factor(Run))) +
  stat_summary(
    fun = mean,
    geom = "bar",
    position = position_dodge(0.9)
  ) +
  stat_summary(
    fun.data = mean_se,
    geom = "errorbar",
    position = position_dodge(0.9),
    width = 0.2
  ) +
  scale_y_continuous(labels = function(x) paste0(round(x * 100, 1), "%"),
                     limits = c(0, 0.04)
                     )+# Set the max y-axis limit to 5% (0.05 is 5%))+
  scale_fill_manual(
    values = c("1" = "grey80", "2" = "grey50", "3" = "grey20")
  ) +
  labs(x = "Voltage", y = "Average Iron % Weight", fill = "Runs") +
  theme_minimal() +
  ggtitle("% Weight Iron by Voltage and Runs (Raw Data)")

  # residual plot of raw data
ggplot(raw_data, aes(x = fitted(diagnostic_fit), y = residuals(diagnostic_fit)/sd(residuals(diagnostic_fit)))) +
  geom_point() +
  geom_hline(yintercept = 0, color = "magenta", linetype = "dashed") +
  ggtitle("Semi-Studentized Residuals vs Fitted Values") +
  xlab("Fitted Values") +
  ylab("Semi-Studentized Residuals")
  
  # linear regression of raw data 
plot(raw_data$Voltage, raw_data$Data, main = "Simple Linear Regression of % Weight of Iron and Voltage Level", xlab = "Voltage (V)", ylab = "% Titanium")
abline(diagnostic_fit)
summary(diagnostic_fit)

## Remove outliers and zeros from data
cleaned_data <- subset(raw_data, abs(residuals(diagnostic_fit)/sd(residuals(diagnostic_fit))) <= 3 & raw_data$Data!=0)
cleaned_aov <- aov(Data ~ Voltage * Run * Puck, data=cleaned_data)
cleaned_lm <- lm(Data ~ Voltage * Run * Puck, data=cleaned_data)

stud_cleaned <-residuals(cleaned_aov)/sd(residuals(cleaned_aov))

# bar chart of cleaned data
ggplot(cleaned_data, aes(x = factor(Voltage), y = Data, fill = factor(Run))) +
  stat_summary(
    fun = mean,
    geom = "bar",
    position = position_dodge(0.9)
  ) +
  stat_summary(
    fun.data = mean_se,
    geom = "errorbar",
    position = position_dodge(0.9),
    width = 0.2
  ) +
  scale_y_continuous(labels = function(x) paste0(round(x * 100, 1), "%"),
                     limits = c(0, 0.04)
  )+# Set the max y-axis limit to 5% (0.05 is 5%))+
  scale_fill_manual(
    values = c("1" = "grey80", "2" = "grey50", "3" = "grey20")
  ) +
  labs(x = "Voltage", y = "Average Iron % Weight", fill = "Runs") +
  theme_minimal() +
  ggtitle("% Weight Iron by Voltage and Runs (Cleaned Data)")

#boxplot of cleaned data
ggplot(cleaned_data, aes(x = factor(Voltage), y = Data, fill = factor(Run))) +
  geom_boxplot()+
  labs(x = "Voltage", y = "Iron % Weight", fill = "Runs") +
  scale_y_continuous(labels = function(x) paste0(round(x * 100, 1), "%"),
                     limits = c(0, 0.15)
  )+# Set the max y-axis limit to 15% (0.05 is 5%))+
  scale_fill_manual(
    values = c("1" = "grey80", "2" = "grey50", "3" = "grey20")
  ) +
  theme_minimal()+
  ggtitle("Iron % Weight by Voltage and Runs \n (Outliers and zeros removed)")



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

# Check for normality Shapiro
shapiro.test(stud_cleaned)
# Q-Q plot
qqnorm(residuals(cleaned_aov))
qqline(residuals(cleaned_aov), col = "red")


### TRANSFORM DATA 
pt <- powerTransform(cleaned_aov, family="bcPower")
cleaned_data$transformed <- bcPower(cleaned_data$Data, pt$lambda)


#cleaned_transformed_aov <- aov(transformed ~ Voltage * Run + Error(Puck/Run), data=cleaned_data)
cleaned_transformed_aov <- aov(transformed ~ Voltage * Run * Puck, data=cleaned_data)

stud_transformed <- residuals(cleaned_transformed_aov)/sd(residuals(cleaned_transformed_aov))

shapiro.test(stud_transformed)
# Q-Q plot of TRANSFORMED data
qqnorm(residuals(cleaned_transformed_aov),title="Normal Q-Q Plot of Cleaned and Transformed Data")
qqline(residuals(cleaned_transformed_aov), col = "red")

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
  ggtitle("Absolute Value of Residuals vs Fitted Values (After Transformation)") +
  xlab("Fitted Values") +
  ylab("Absolute Value of Semi-Studentized Residuals")

summary(cleaned_transformed_aov)
summary(cleaned_transformed_lm)

###### ANOVA THAT ACTUALLY SHOWS THE REPEATED MEASURES DESIGN
ezANOVA(data=cleaned_data,dv=transformed,wid=Puck,within=Run,between=Voltage,detailed=TRUE)

############ IF YOU WANT TO AGGREGATE DATA (condense it)
aggregated_data <- aggregate(transformed ~ Voltage * Run * Puck, data=cleaned_data, FUN=mean) 
# ^ collapses all 15 measurements per voltage*run*puck combo into 1 point.

# Spearman rank correlation test
cor.test(abs(residuals(cleaned_transformed_aov)), fitted(cleaned_transformed_aov), method = "spearman")

# Levene Test for Homo Variance
library(car)
leveneTest(transformed ~ Voltage, data=cleaned_data)
leveneTest(transformed ~ Puck, data=cleaned_data) 
leveneTest(transformed ~ Run, data=cleaned_data)
leveneTest(transformed ~ interaction(vo,puck,run), data=data_clean)

TukeyHSD(cleaned_transformed_aov)



## Try to make independent

independent_data <- subset(raw_data,raw_data$Puck%%3==raw_data$Run%%3)
independent_data <- subset(independent_data,independent_data$Data!=0) # remove zeros (dropped points) 
independent_data$Voltage <- as.factor(independent_data$Voltage)
independent_data$Run <- as.factor(independent_data$Run)

independent_lm <- lm(Data ~ Voltage * Run,data=independent_data)
summary(independent_lm)
stud_independent <- residuals(independent_lm)/sd(residuals(independent_lm))

# independent histogram
ggplot(independent_data, aes(x = Data)) +
  geom_histogram(binwidth = 0.005, fill = "blue", color = "black", alpha = 0.7) +
  ggtitle("Histogram of % Iron") +
  xlab("Iron (%)") +
  scale_x_continuous(labels = scales::percent) +
  ylab("Frequency")

#independent boxplot (non transformed)
ggplot(independent_data, aes(x = factor(Voltage), y = Data, fill = factor(Run))) +
  geom_boxplot()+
  labs(x = "Voltage", y = "Iron % Weight", fill = "Runs") +
  scale_y_continuous(labels = function(x) paste0(round(x * 100, 1), "%"),
                     limits = c(0, 0.15)
  )+# Set the max y-axis limit to 15% (0.05 is 5%))+
  scale_fill_manual(
    values = c("1" = "grey80", "2" = "grey50", "3" = "grey20")
  ) +
  theme_minimal()+
  ggtitle("Iron % Weight by Voltage and Runs")

# Independent residuals
ggplot(independent_data, aes(x = fitted(independent_lm), y = stud_independent)) +
  geom_point() +
  geom_smooth(method = "lm", color = "blue", se = FALSE) +
  scale_y_continuous(limits = c(-3, 3) )+
  ggtitle("Semi-Studentized Residuals vs Fitted Values (Independent)") +
  xlab("Fitted Values") +
  ylab("Semi-Studentized Residuals")
## QQ and normality of independent residuals
qqnorm(residuals(independent_lm),title="Normal Q-Q Plot of Independent, Zeroless Data")
qqline(residuals(independent_lm), col = "red")
shapiro.test(residuals(independent_lm))

#transformation of independent
pt2 <- powerTransform(independent_lm, family="bcPower")
independent_data$transformed <- bcPower(independent_data$Data, pt2$lambda)
independent_transformed_lm <- lm(transformed ~ Voltage * Run,data=independent_data)
independent_transformed_aov <- aov(transformed ~ Voltage * Run,data=independent_data)
summary(independent_transformed_aov)
stud_independent_transformed <- residuals(independent_transformed_lm)/sd(residuals(independent_transformed_lm))

#independent boxplot (transformed)
ggplot(independent_data, aes(x = factor(Voltage), y = transformed, fill = factor(Run))) +
  geom_boxplot()+
  labs(x = "Voltage", y = "Transformed Iron % Weight (lambda = 0.0519)", fill = "Runs") +
  # Set the max y-axis limit to 15% (0.05 is 5%))+
  scale_fill_manual(
    values = c("1" = "grey80", "2" = "grey50", "3" = "grey20")
  ) +
  theme_minimal()+
  ggtitle("Transformed Iron % Weight (lambda = 0.0519) by Voltage and Runs")

#independent transformed residuals 
ggplot(independent_data, aes(x = fitted(independent_transformed_lm), y = stud_independent_transformed)) +
  geom_point() +
  geom_smooth(method = "lm", color = "blue", se = FALSE) +
  scale_y_continuous(limits = c(-3, 3) )+
  ggtitle("Semi-Studentized Residuals vs Fitted Values (Independent & Transformed)") +
  xlab("Fitted Values") +
  ylab("Semi-Studentized Residuals")

# normality of independent transformed 
shapiro.test(residuals(independent_transformed_lm))
qqnorm(residuals(independent_transformed_lm),main="Normal Q-Q Plot of Independent and Transformed Data")
qqline(residuals(independent_transformed_lm), col = "red")

# test for homoscedasticity 
bartlett.test(transformed ~ Voltage, data=independent_data)
bartlett.test(transformed ~ Run, data=independent_data)
independent_data$group <- interaction(independent_data$Voltage, independent_data$Run)
bartlett.test(transformed ~ group, data =independent_data)

