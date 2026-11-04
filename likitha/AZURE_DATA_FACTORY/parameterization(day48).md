# Azure Data Factory – Parameters, Variables and Expressions

### 1. Pipeline Parameters vs Variables vs System Variables

ADF uses parameters and variables to make pipelines dynamic and reusable.

- **Pipeline Parameters:** Values passed into a pipeline from outside or during execution. They are read-only and cannot be changed once the pipeline starts. Example: database name, file name, folder path.
- **Pipeline Variables:** Values stored inside a pipeline that can be changed during execution using activities like Set Variable and Append Variable. Example: counters, temporary values, status flags.
- **System Variables:** Built-in values provided by ADF. They are read-only and give information about the current execution. Example: `pipeline().Pipeline`, `pipeline().RunId`, `pipeline().TriggerTime`.

**Remember:** Parameters = Input values, Variables = Changeable values, System variables = ADF-provided information.

### 2. Dynamic Content and Expression Builder

Dynamic content allows us to generate values at runtime instead of hardcoding them.

ADF expressions start with `@`. We can use parameters, variables, system variables and functions inside expressions.

Examples:
- `@pipeline().parameters.FileName`
- `@variables('FolderName')`
- `@pipeline().RunId`

**Expression Builder:** It helps us write expressions by selecting available parameters, variables and functions. It also helps reduce syntax mistakes.

There are two common ways to use expressions:

- **Expression:** `@pipeline().parameters.FileName` – evaluates to the actual value.
- **String interpolation:** `File name is @{pipeline().parameters.FileName}` – combines normal text with a dynamic value.

### 3. Everyday ADF Functions

ADF provides built-in functions to perform common operations.

| Function | Purpose / Example |
|---|---|
| `concat()` | Joins strings. `@concat('Data_', 'File')` → Data_File |
| `formatDateTime()` | Formats date and time. `@formatDateTime(utcNow(),'yyyy-MM-dd')` |
| `utcNow()` | Returns current UTC date and time. |
| `addDays()` | Adds or subtracts days. `@addDays(utcNow(),-1)` → Yesterday |
| `if()` | Checks a condition and returns one of two values. `@if(equals(1,1),'Yes','No')` |
| `coalesce()` | Returns the first non-null value. `@coalesce(pipeline().parameters.Name,'Default')` |
| `item()` | Returns the current item being processed inside a ForEach loop. `@item()` |

**Important:** `item()` is especially useful in ForEach loops. If the loop receives a list of file names, `@item()` represents the current file name in each iteration.

### 4. Parameterized Datasets and Linked Services – One Pipeline for Many Inputs

Parameterization allows us to reuse the same pipeline for different databases, tables, files and folders instead of creating separate pipelines for every input.

- **Parameterized Dataset:** Makes dataset properties such as file name, folder path, table name or database name dynamic.
- **Parameterized Linked Service:** Makes connection properties such as server name or database name dynamic.

**How the mapping works:**

1. Create parameters in the pipeline.
2. Create parameters in the dataset or linked service.
3. Pass pipeline parameter values into dataset/linked service parameters.
4. Use those parameters inside the dataset or linked service through dynamic expressions.
5. During execution, ADF evaluates the expressions and connects to the correct source or destination.

**Example:** A ForEach loop receives file names from a list. Each iteration passes its current `@item()` value to the dataset's FileName parameter. The same Copy Activity copies each file without creating separate activities.

### 5. Debugging Expression Errors

Most expression errors happen because of incorrect syntax, data types, null values or missing brackets.

- **String vs Integer:** Strings must be enclosed in single quotes inside expressions. Numbers should not be quoted. Example: `'100'` is a string, whereas `100` is an integer.
- **Null Values:** A parameter may have no value. Use `coalesce()` to provide a default value when appropriate.
- **Quotes:** Use single quotes for string literals inside ADF expressions. Example: `@concat('File_', '01')`.
- **Brackets:** Always check opening and closing parentheses, quotation marks and square brackets. Incorrect nesting can cause expression errors.
- **Type mismatch:** An integer cannot always be used where a string is expected. Use conversion functions when required, such as `string()` or `int()`.
- **Expression syntax:** Check whether the expression starts with `@` and whether the function arguments are correct.

**Debugging tip:** Check the expression, parameter value, expected data type and actual evaluated value before changing the entire pipeline.

### 6. Check Evaluated Values in Activity Input JSON in Monitor

ADF allows us to inspect the actual values passed to an activity during execution.

Steps:
1. Run the pipeline using Debug or Trigger.
2. Open the **Monitor** section.
3. Go to Pipeline Runs and select the required pipeline run.
4. Open the activity details.
5. Select **Input** to view the activity's Input JSON.

The Input JSON shows the evaluated values that ADF actually passed to the activity, rather than just the original dynamic expressions.

**Example:** If the dataset expression is `@pipeline().parameters.FileName` and the parameter value is `sales.csv`, the evaluated input should show `sales.csv`.

This is useful for identifying incorrect file paths, wrong database names, unexpected null values and incorrect parameter mappings.

**Remember:** Debug helps us test the pipeline, while Monitor helps us inspect actual execution details and understand what values were passed to each activity.