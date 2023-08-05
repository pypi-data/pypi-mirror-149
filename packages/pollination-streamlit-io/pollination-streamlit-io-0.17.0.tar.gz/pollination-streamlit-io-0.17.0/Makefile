.PHONY: generate-frontend

.PHONY: dev-install-package

.PHONY: copy-build

generate-frontend:
	npm run build --prefix dev/send_button/st_po_send_geometry/frontend
	npm run build --prefix dev/get_button/st_po_get_geometry/frontend
	npm run build --prefix dev/command_button/st_po_run_command/frontend
	npm run build --prefix dev/send_checkbox/st_po_send_checkbox/frontend
	npm run build --prefix dev/special_sync/st_po_special_sync/frontend
	npm run build --prefix dev/send_settings/st_po_send_settings/frontend

dev-install-package:
	cd tests/PollinationButtonsTest && \
	pip install -e ../.

copy-build:
	rm -rf pollination_streamlit_io/button/command/*
	rm -rf pollination_streamlit_io/button/get/*
	rm -rf pollination_streamlit_io/button/send/*
	rm -rf pollination_streamlit_io/inputs/send/*
	rm -rf pollination_streamlit_io/special/sync/*
	rm -rf pollination_streamlit_io/special/settings/*
	cp -r dev/command_button/st_po_run_command/frontend/build/. pollination_streamlit_io/button/command/
	cp -r dev/get_button/st_po_get_geometry/frontend/build/. pollination_streamlit_io/button/get/
	cp -r dev/send_button/st_po_send_geometry/frontend/build/. pollination_streamlit_io/button/send/
	cp -r dev/send_checkbox/st_po_send_checkbox/frontend/build/. pollination_streamlit_io/inputs/send/
	cp -r dev/special_sync/st_po_special_sync/frontend/build/. pollination_streamlit_io/special/sync/
	cp -r dev/send_settings/st_po_send_settings/frontend/build/. pollination_streamlit_io/special/settings/
