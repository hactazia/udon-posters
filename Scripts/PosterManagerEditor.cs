#if UNITY_EDITOR
using System;
using UnityEditor;
using UnityEditor.UIElements;
using UnityEngine;
using UnityEngine.UIElements;
using VRC.SDKBase;

namespace Hactazia.Posters {
	[CustomEditor(typeof(PosterManager))]
	public class PosterManagerEditor : Editor {
		private const string BaseUrl    = "http://localhost:8000/atlas";
		private const int    AtlasCount = 128;

		private VisualElement        _root;
		private TextField            _base;
		private UnsignedIntegerField _count;
		private PropertyField        _material;

		private PosterManager Manager
			=> target as PosterManager;

		private static Poster[] Posters
			=> FindObjectsOfType<Poster>();

		public override VisualElement CreateInspectorGUI() {
			if (_root != null) return _root;
			_root = Resources.Load<VisualTreeAsset>("PosterManagerEditor").CloneTree();

			_base        = _root.Q<TextField>("base");
			_count       = _root.Q<UnsignedIntegerField>("count");
			_material    = _root.Q<PropertyField>("material");
			_base.value  = Manager.metaUrl?.Get() ?? BaseUrl;
			_count.value = (uint)(Manager.atlasUrls?.Length ?? AtlasCount);
			UpdateContent();
			_base.RegisterValueChangedCallback(OnBaseChanged);
			_count.RegisterValueChangedCallback(OnCountChanged);
			_material.BindProperty(serializedObject.FindProperty(nameof(PosterManager.material)));

			return _root;
		}

		private void UpdateContent() {
			if (_base == null || _count == null) return;
			var baseUrl = _base.value.TrimEnd('/');
			if (string.IsNullOrEmpty(baseUrl))
				baseUrl = BaseUrl;
			var count = _count.value;
			if (count < 1)
				count = AtlasCount;
			Manager.metaUrl   = new VRCUrl(baseUrl);
			Manager.atlasUrls = new VRCUrl[count];
			for (var i = 0; i < count; i++)
				Manager.atlasUrls[i] = new VRCUrl($"{baseUrl}/{i}");
			Manager.posters = Posters;
			_base.SetValueWithoutNotify(baseUrl);
			_count.SetValueWithoutNotify(count);
			EditorUtility.SetDirty(Manager);
		}

		private void OnBaseChanged(ChangeEvent<string> evt)
			=> UpdateContent();

		private void OnCountChanged(ChangeEvent<uint> evt)
			=> UpdateContent();

		private static void OnHierarchyChanged() {
			var manager = FindObjectOfType<PosterManager>();
			if (!manager) return;
			manager.posters = FindObjectsOfType<Poster>();
			EditorUtility.SetDirty(manager);
		}

		[InitializeOnLoadMethod]
		public static void Initialize() {
			EditorApplication.hierarchyChanged += OnHierarchyChanged;
		}
	}
}
#endif