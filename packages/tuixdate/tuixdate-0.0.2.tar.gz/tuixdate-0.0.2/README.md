# Tuixdate

Console Tuix timesheet tool.

# Install
Install from package
```
pip3 install requests
pip3 install tuixdate
```

Note: user python >= 3.7 and pip3 -> pip

```
pip3 install git+https://github.com/tuixdevelopment/tuixdate
```

For develop:

```
git clone https://github.com/tuixdevelopment/tuixdate
cd tuixdate
pip3 install -e .
```

## Add to PATH environment
```
export PATH=$HOME/.local/bin:$PATH
```

## Login
```
tuixdate login <your_tuix_username>
```

## Daily work record (current day)
```
tuixdate push "Project" "8:00" "18:00" 60 "Comments"
```

## Update work record by date
```
tuixdate push "Project Name" "8:00" "18:00" 60 "Comments" "2021-11-29"
```

## Clean work record (current day) 
```
tuixdate clean "Project Name"
```

## Clean work record by date 
```
tuixdate clean "Project Name" "2021-11-29"
```

## List timesheet (current month)
```
tuixdate timesheet "Project Name"
```

## List timesheet by month
```
tuixdate timesheet "Project Name" "2021-10"
```

## List timesheet by day
```
tuixdate timesheet "Project Name" "2021-10-25"
```