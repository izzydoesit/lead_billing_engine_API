## **Evaluation Criteria Scorecard**

### **Main Evaluation**

| **Category**                | **⭐️1 - Needs Improvement**                                                                                                                                                           | **⭐️2 - Meets Expectations**                                                                                                                                                        | **⭐️3 - Exceeds Expectations**                                                                                                                                                           |
|-----------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Infrastructure as Code** | - Incomplete or incorrect Terraform scripts.<br>- Essential services not provisioned.<br>- Major configuration issues.                                                                  | - Basic Terraform scripts with some services provisioned.<br>- Minor configuration issues.<br>- Limited use of modules.                                                              | - Well-organized Terraform scripts provisioning all required services correctly.<br>- Efficient use of modules.<br>- Adheres to best practices.                                          |
| **Backend Development**    | - Missing or non-functional GET /billingReports endpoint.<br>- Poor code structure with significant issues.<br>- Does not follow clean code practices or design patterns.                  | - Functional GET /billingReports endpoint.<br>- Acceptable code structure with some areas for improvement.<br>- Generally follows clean code practices and design patterns.             | - Fully functional and optimized GET /billingReports endpoint.<br>- Excellent code structure using appropriate design patterns.<br>- Exemplary clean code with high maintainability.     |
| **Billing Logic**          | - Incorrect or incomplete implementation of billing rules.<br>- Major business rules missing or flawed.<br>- Logic does not handle duplicates or caps effectively.                          | - Partial implementation of billing rules.<br>- Some business rules correctly implemented, others missing or incorrect.<br>- Basic handling of duplicates and caps.                    | - Accurately implements all specified business rules with efficient and optimized logic.<br>- Comprehensive handling of duplicates and caps.<br>- Clear and maintainable billing logic.     |
| **Database Design**        | - Poorly designed schema.<br>- Lack of normalization.<br>- Inappropriate relationships or missing constraints.                                                                             | - Basic schema with some normalization issues.<br>- Some relationships or constraints missing or incorrect.<br>- Partial use of ORM features.                                           | - Well-designed schema with proper normalization and relationships.<br>- Few minor issues.<br>- Effective use of ORM features with seamless migrations.                                   |
| **Deployment Automation**  | - Incomplete or non-functional deployment scripts.<br>- Manual steps required.<br>- Lack of automation for key processes.                                                                  | - Basic deployment scripts with some automation.<br>- Some manual steps still necessary.<br>- Limited error handling in scripts.                                                         | - Comprehensive deployment scripts automating setup, deployment, and migrations.<br>- Robust error handling.<br>- Clear and maintainable scripts with full automation.                     |
| **Documentation**          | - Inadequate or missing documentation.<br>- Hard to understand or follow.<br>- Missing key sections (setup, API docs, billing logic).                                                        | - Basic documentation covering some aspects.<br>- Lacks clarity or completeness.<br>- Missing some key sections.                                                                         | - Comprehensive README with clear setup instructions, API documentation, and billing logic explanations.<br>- Well-organized and easy to follow with all necessary details.                  |

### **Bonus Points**

| **Bonus Category**           | **⭐️0 - Not Attempted**                                                                                  | **⭐️1 - Partial**                                                                                                                                            | **⭐️2 - Full**                                                                                                                                                     |
|------------------------------|-----------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Unit Testing**             | - No unit tests provided.<br>- Lacks any testing framework integration.                                 | - Basic unit tests covering some functionality.<br>- Partial coverage of critical paths.                                                                       | - Comprehensive unit tests covering critical paths and billing logic.<br>- Well-organized and pass successfully.                                                    |
| **API Gateway Integration**  | - No API Gateway setup.<br>- Incomplete or non-functional integration.                                  | - Basic API Gateway setup with some API integration.<br>- Limited routing configuration.                                                                        | - Fully integrated API Gateway with robust API development and seamless routing.<br>- Properly configured and functional.                                             |

---

## **Scoring Guidelines**

### **Main Evaluation Categories**

- **⭐️1 - Needs Improvement:** The candidate's submission lacks fundamental components or contains major flaws that prevent functionality.

- **⭐️2 - Meets Expectations:** The submission includes required components and functions correctly but has some issues or areas for improvement.

- **⭐️3 - Exceeds Expectations:** The candidate delivers a solution that fully meets and exceeds all requirements with exceptional quality, including optimized implementations and best practices.

### **Bonus Categories**

- **⭐️0 - Not Attempted:** The candidate did not work on this bonus criterion.

- **⭐️1 - Partial:** The submission includes some aspects of the bonus criteria but lacks completeness or depth.

- **⭐️2 - Full:** The candidate fully meets the bonus criteria with comprehensive and high-quality implementations.

---
