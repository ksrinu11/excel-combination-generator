from fastapi import FastAPI, File, UploadFile, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
import itertools
import os
from typing import List, Optional
import json
import uuid
from pathlib import Path

app = FastAPI()

# Create directories if they don't exist
os.makedirs("templates", exist_ok=True)
os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    output_directory: str = Form(...),
    output_filename: str = Form(...),
    selected_columns: str = Form(...)
):
    try:
        # Save uploaded file
        file_id = str(uuid.uuid4())
        file_path = f"uploads/{file_id}_{file.filename}"
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Read Excel file
        df = pd.read_excel(file_path)
        
        # Parse selected columns from JSON
        columns_for_combination = json.loads(selected_columns)
        
        if not columns_for_combination:
            raise HTTPException(status_code=400, detail="At least one column must be selected for combinations")
        
        # Validate columns exist in DataFrame
        invalid_cols = [col for col in columns_for_combination if col not in df.columns]
        if invalid_cols:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid columns: {invalid_cols}"
            )
        
        # Get unique values for each selected column
        unique_values = {}
        for col in columns_for_combination:
            # Get unique values and convert NaN to empty string for consistency
            unique_vals = df[col].fillna("").unique().tolist()
            # Remove empty strings if they were originally NaN, unless user wants them
            unique_values[col] = [val for val in unique_vals if val != ""] if "" in unique_vals and len(unique_vals) > 1 else unique_vals
        
        # Generate all combinations for selected columns
        combinations = list(itertools.product(*[unique_values[col] for col in columns_for_combination]))
        
        # Create result DataFrame with the right number of rows
        num_combinations = len(combinations)
        num_original_rows = len(df)
        
        # Create empty DataFrame with same structure as original
        combo_df = pd.DataFrame(index=range(num_combinations), columns=df.columns)
        
        # Fill selected columns with combinations
        for i, combination in enumerate(combinations):
            for j, col in enumerate(columns_for_combination):
                combo_df.iloc[i, combo_df.columns.get_loc(col)] = combination[j]
        
        # Fill unselected columns with original data (only for existing rows)
        unselected_columns = [col for col in df.columns if col not in columns_for_combination]
        for i in range(num_combinations):
            if i < num_original_rows:
                # Use original data for this row
                for col in unselected_columns:
                    combo_df.iloc[i, combo_df.columns.get_loc(col)] = df.iloc[i][col]
            else:
                # Leave empty for extra rows
                for col in unselected_columns:
                    combo_df.iloc[i, combo_df.columns.get_loc(col)] = ""
        
        # Create output directory if it doesn't exist
        output_dir = f"outputs/{output_directory}"
        os.makedirs(output_dir, exist_ok=True)
        
        # Save to Excel file
        if not output_filename.endswith('.xlsx'):
            output_filename += '.xlsx'
            
        output_file_path = f"{output_dir}/{output_filename}"
        combo_df.to_excel(output_file_path, index=False)
        
        # Clean up uploaded file
        os.remove(file_path)
        
        return {
            "success": True,
            "message": f"Combinations generated successfully! Total combinations: {len(combo_df)}",
            "output_file": output_file_path,
            "download_url": f"/download/{output_directory}/{output_filename}",
            "total_combinations": len(combo_df)
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/download/{directory}/{filename}")
async def download_file(directory: str, filename: str):
    file_path = f"outputs/{directory}/{filename}"
    if os.path.exists(file_path):
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    else:
        raise HTTPException(status_code=404, detail="File not found")

@app.post("/get-columns")
async def get_columns(file: UploadFile = File(...)):
    try:
        # Save temporary file
        temp_path = f"uploads/temp_{file.filename}"
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Read Excel file to get columns
        df = pd.read_excel(temp_path)
        columns = df.columns.tolist()
        
        # Get sample data for preview and handle NaN values
        sample_df = df.head(5).fillna("")  # Replace NaN with empty strings
        sample_data = sample_df.to_dict('records')
        
        # Clean up temp file
        os.remove(temp_path)
        
        return {
            "columns": columns,
            "sample_data": sample_data,
            "total_rows": len(df)
        }
        
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)