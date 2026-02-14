#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import os
import re

def main():
    module = AnsibleModule(
        argument_spec=dict(
            port=dict(type='int', required=True),
            config_path=dict(type='str', default='/etc/nginx/sites-available/default')
        )
    )

    port = module.params['port']
    config_path = module.params['config_path']
    changed = False
    
    if not os.path.exists(config_path):
        config_content = f"""server {{
    listen {port};
    server_name localhost;
    
    location / {{
        root /var/www/html;
        index index.html;
    }}
}}"""
        with open(config_path, 'w') as f:
            f.write(config_content)
        changed = True
    else:
        with open(config_path, 'r') as f:
            content = f.read()
        
        new_content = re.sub(r'listen\s+\d+;', f'listen {port};', content)
        
        if new_content != content:
            with open(config_path, 'w') as f:
                f.write(new_content)
            changed = True
    
    module.exit_json(changed=changed, port=port, config_path=config_path)

if __name__ == '__main__':
    main()